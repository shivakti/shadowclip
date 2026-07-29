import os
import subprocess
import librosa
import numpy as np
from pathlib import Path
from typing import List, Tuple


class ShadowClipSegmenter:
    """Generate highlight video segments based on audio peaks"""

    def __init__(
        self,
        min_duration: float = 30.0,
        max_duration: float = 60.0,
        peak_percentile: float = 90.0,
    ):
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.peak_percentile = peak_percentile

    # --------------------------------------------------
    # AUDIO EXTRACTION
    # --------------------------------------------------

    def extract_audio_features(self, video_path: str) -> Tuple[np.ndarray, float]:
        y, sr = librosa.load(video_path, sr=None, mono=True)
        return y, sr

    # --------------------------------------------------
    # MAIN SEGMENT GENERATION
    # --------------------------------------------------

    def generate_segments(
        self,
        video_path: str,
        output_dir: str,
        prefix: str = "segment",
        max_segments: int = 5,
    ) -> List[str]:

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        print(f"Analyzing {video_path}...")
        y, sr = self.extract_audio_features(video_path)
        duration = len(y) / sr

        print(f"📊 Video duration: {duration/60:.1f} minutes")
        print(f"🎯 Target clips: {max_segments}")

        # --- Detect peaks ---
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)

        peaks = librosa.util.peak_pick(
            onset_env,
            pre_max=3,
            post_max=3,
            pre_avg=3,
            post_avg=5,
            delta=0.5,
            wait=20,
        )

        if len(peaks) == 0:
            raise RuntimeError("No audio peaks detected.")

        peak_times = librosa.frames_to_time(peaks, sr=sr)
        peak_strengths = onset_env[peaks]

        # Filter strongest peaks
        threshold = np.percentile(peak_strengths, self.peak_percentile)
        strong_peaks = [
            (t, s)
            for t, s in zip(peak_times, peak_strengths)
            if s >= threshold
        ]

        if not strong_peaks:
            raise RuntimeError("No strong peaks found.")

        # Sort by strength descending
        strong_peaks.sort(key=lambda x: x[1], reverse=True)

        selected_segments = []
        min_gap = 50  # Minimum separation between clips (seconds)

        # --- Build segments ---
        for peak_time, strength in strong_peaks:

            start = max(0, peak_time - 20)
            end = min(duration, peak_time + 20)

            clip_duration = end - start

            # Enforce duration bounds
            if clip_duration < self.min_duration:
                end = min(duration, start + self.min_duration)
                clip_duration = end - start

            if clip_duration > self.max_duration:
                end = start + self.max_duration
                clip_duration = end - start

            # Check overlap with previously selected clips
            overlap = False
            for s, e in selected_segments:
                if not (end + min_gap < s or start - min_gap > e):
                    overlap = True
                    break

            if not overlap:
                selected_segments.append((start, end))

            if len(selected_segments) >= max_segments:
                break

        if not selected_segments:
            raise RuntimeError("No valid highlight segments found.")

        # --- Extract segments ---
        output_paths = []

        for i, (start, end) in enumerate(selected_segments):
            output_path = os.path.join(
                output_dir,
                f"{prefix}_{i+1:03d}.mp4"
            )

            self._extract_segment_ffmpeg(
                video_path,
                output_path,
                start,
                end - start,
            )

            print(
                f"Created highlight {i+1}: "
                f"{start:.1f}s - {end:.1f}s"
            )

            output_paths.append(output_path)

        return output_paths

    # --------------------------------------------------
    # FFMPEG EXTRACTION
    # --------------------------------------------------

    def _extract_segment_ffmpeg(
        self,
        input_path: str,
        output_path: str,
        start_time: float,
        duration: float,
    ):

        cmd = [
            "ffmpeg",
            "-i",
            input_path,
            "-ss",
            str(start_time),
            "-t",
            str(duration),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-y",
            output_path,
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)