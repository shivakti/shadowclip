import random

class AIContentGenerator:

    def __init__(self):

        self.power_words = [
            "SECRET", "TRUTH", "WARNING", "POWER", "CONTROL",
            "MONEY", "MIND", "SYSTEM", "REALITY", "HIDDEN"
        ]

        self.hook_patterns = [
            "THIS IS WHY YOU FAIL",
            "NOBODY TELLS YOU THIS",
            "YOU ARE BEING LIED TO",
            "THIS CONTROLS YOUR LIFE",
            "YOU'RE LOSING MONEY",
            "THIS CHANGES EVERYTHING",
            "WAKE UP NOW",
            "THE SYSTEM IS BROKEN",
            "YOU NEED TO SEE THIS"
        ]

    # ----------------------------

    def generate_hook(self, text, video_type):

        base = random.choice(self.hook_patterns)

        if video_type == "face":
            return f"{base}"

        if video_type == "slides":
            return f"{base}"

        return base

    # ----------------------------

    def generate_description(self, hook):

        return f"""
🔥 {hook}

This video will change how you see reality.

Follow for more.
        """.strip()

    # ----------------------------

    def generate_hashtags(self, video_type):

        base = ["#viral", "#mindset", "#money", "#success"]

        if video_type == "face":
            base += ["#creator", "#personalbrand"]

        if video_type == "slides":
            base += ["#education", "#learning"]

        return base