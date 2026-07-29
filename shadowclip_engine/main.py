import time
import shutil
import json
from pathlib import Path

from segments import ShadowClipSegmenter
from video import convert_to_vertical
from speech import ShadowSpeechAnalyzer
from thumbnail import ShadowThumbnailGenerator

from video_intelligence import VideoIntelligence
from ai_content_generator import AIContentGenerator

# ----------------------------
# METADATA
# ----------------------------

def create_metadata(clip_number: int, clip_folder: Path, hook: str, description: str, hashtags: list):

    metadata = {
        "title": hook,
        "description": description,
        "hashtags": hashtags,
        "clip_number": clip_number,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(clip_folder / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)


# ----------------------------
# MAIN PIPELINE
# ----------------------------

def main(video_path: str, output_root: str = "./output"):

    start_time = time.time()

    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    temp_dir = output_root / "temp_horizontal"

    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    try:

        print(f"\n🎬 Processing: {video_path.name}")

        # --------------------------------
        # SEGMENTATION
        # --------------------------------

        segmenter = ShadowClipSegmenter(min_duration=25.0, max_duration=45.0)

        horizontal_segments = segmenter.generate_segments(
            str(video_path),
            str(temp_dir),
            prefix="horizontal",
            max_segments=5
        )

        if not horizontal_segments:
            raise RuntimeError("No segments generated")

        print(f"✅ Segments: {len(horizontal_segments)}")

        # --------------------------------
        # LOAD AI (ONCE)
        # --------------------------------

        speech = ShadowSpeechAnalyzer("base")
        intelligence = VideoIntelligence()
        thumb_gen = ShadowThumbnailGenerator()
        content_ai = AIContentGenerator()

        print("\n🚀 Generating clips...\n")

        # --------------------------------
        # LOOP
        # --------------------------------

        for i, horiz_path in enumerate(horizontal_segments, 1):

            clip_folder = output_root / f"clip_{i:03d}"
            clip_folder.mkdir(parents=True, exist_ok=True)

            horiz_dest = clip_folder / "horizontal.mp4"
            shutil.move(horiz_path, horiz_dest)

            vert_dest = clip_folder / "vertical.mp4"

            # 🎥 Convert
            print(f"Clip {i:03d} | Vertical...", end="")
            convert_to_vertical(str(horiz_dest), str(vert_dest))
            print(" ✓")

            # 🧠 Transcribe
            print(f"Clip {i:03d} | Transcribe...", end="")
            text = speech.transcribe(str(vert_dest))
            print(" ✓")

            # 🔍 Analyze video
            video_type = intelligence.analyze_video(str(vert_dest))

            # 🤖 AI CONTENT (REAL THINKING HERE)
            hook = content_ai.generate_hook(text, video_type)
            description = content_ai.generate_description(hook)
            hashtags = content_ai.generate_hashtags(video_type)

            print(f"Clip {i:03d} | Hook → {hook}")

            # 🖼️ Thumbnail
            thumb_dest = clip_folder / "thumbnail.jpg"

            print(f"Clip {i:03d} | Thumbnail...", end="")
            thumb_gen.generate_thumbnail(str(vert_dest), str(thumb_dest), hook)
            print(" ✓")

            # 📦 Metadata
            create_metadata(i, clip_folder, hook, description, hashtags)

        # cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        print("\n🔥 DONE 🔥")
        print(f"📁 Output: {output_root.absolute()}")

    except Exception as e:

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        print("\n❌ ERROR:", e)
        raise


# ----------------------------
# CLI
# ----------------------------

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("video_path", nargs="?", default=None)
    parser.add_argument("--output", default="./output")

    args = parser.parse_args()

    if args.video_path is None:

        input_dir = Path("./input")
        videos = list(input_dir.glob("*.mp4"))

        if not videos:
            raise FileNotFoundError("No videos found in /input")

        video_to_process = videos[0]
        print(f"🎥 Using: {video_to_process.name}")

    else:
        video_to_process = Path(args.video_path)

    main(str(video_to_process), args.output)S