import whisper
import re


class ShadowSpeechAnalyzer:
    """
    Transcribe clips and extract powerful hook phrases
    Optimized for CPU usage
    """

    def __init__(self, model_size: str = "base"):
        print("🔊 Loading Whisper model...")
        self.model = whisper.load_model(model_size)
        print("✅ Whisper model loaded")

    # --------------------------------------------------
    # TRANSCRIPTION
    # --------------------------------------------------

    def transcribe(self, video_path: str) -> str:
        result = self.model.transcribe(video_path)
        text = result["text"].strip()
        return text

    # --------------------------------------------------
    # HOOK EXTRACTION
    # --------------------------------------------------

    def extract_hook(self, text: str) -> str:
        """
        Extracts the most powerful sentence based on simple heuristics
        """

        sentences = re.split(r'[.!?]', text)

        if not sentences:
            return "WATCH THIS"

        power_words = [
            "never", "always", "truth", "secret",
            "money", "fear", "fail", "success",
            "why", "how", "biggest", "mistake",
            "nobody", "everyone"
        ]

        best_sentence = ""
        best_score = 0

        for sentence in sentences:
            s = sentence.strip()
            if len(s) < 20:
                continue

            score = 0
            for word in power_words:
                if word.lower() in s.lower():
                    score += 2

            score += min(len(s) / 100, 2)

            if score > best_score:
                best_score = score
                best_sentence = s

        if not best_sentence:
            best_sentence = sentences[0].strip()

        hook = best_sentence.upper()

        # Limit words for thumbnail
        words = hook.split()
        if len(words) > 8:
            hook = " ".join(words[:8])

        return hook