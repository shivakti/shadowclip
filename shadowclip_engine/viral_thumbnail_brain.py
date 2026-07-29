import random


class ViralThumbnailBrain:

    def __init__(self):

        self.finance_words = [
            "money", "rich", "million", "broke", "income",
            "wealth", "cash", "profit", "finance"
        ]

        self.shock_words = [
            "secret", "truth", "nobody", "never",
            "mistake", "warning"
        ]

        self.power_words = [
            "now", "fast", "today", "instantly"
        ]

    # -----------------------------
    # Detect topic
    # -----------------------------

    def detect_topic(self, hook):

        text = hook.lower()

        for word in self.finance_words:
            if word in text:
                return "finance"

        for word in self.shock_words:
            if word in text:
                return "shock"

        for word in self.power_words:
            if word in text:
                return "power"

        return "general"

    # -----------------------------
    # Choose color
    # -----------------------------

    def choose_color(self, topic):

        if topic == "finance":
            return (0, 255, 120)

        if topic == "shock":
            return (255, 60, 60)

        if topic == "power":
            return (255, 200, 0)

        return random.choice([
            (255, 255, 0),
            (0, 255, 255),
            (255, 80, 80),
            (0, 255, 120),
            (255, 150, 0),
        ])

    # -----------------------------
    # Choose style
    # -----------------------------

    def choose_style(self):

        styles = [
            "impact",
            "box",
            "minimal",
            "big_text",
            "youtube"
        ]

        return random.choice(styles)

    # -----------------------------
    # Optimize hook length
    # -----------------------------

    def optimize_hook(self, hook):

        hook = hook.strip()

        if len(hook) > 40:
            hook = hook[:40]

        words = hook.split()

        if len(words) > 6:
            hook = " ".join(words[:6])

        return hook.upper()

    # -----------------------------
    # Main decision
    # -----------------------------

    def analyze(self, hook):

        topic = self.detect_topic(hook)

        color = self.choose_color(topic)

        style = self.choose_style()

        hook = self.optimize_hook(hook)

        return {
            "hook": hook,
            "topic": topic,
            "color": color,
            "style": style
        }