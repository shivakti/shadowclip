import random


class AIHookWriter:

    def __init__(self):

        self.patterns = [

            "THE TRUTH ABOUT {topic}",
            "WHY YOU ARE STILL {pain}",
            "THIS WILL CHANGE YOUR {area}",
            "NOBODY TELLS YOU THIS ABOUT {topic}",
            "THIS IS WHY YOU FAIL AT {topic}",
            "THE SECRET OF {topic}",
            "THIS WILL MAKE YOU {result}",
        ]

        self.words = {
            "topic": ["MONEY", "DISCIPLINE", "SUCCESS", "FOCUS"],
            "pain": ["BROKE", "LOST", "STUCK", "WEAK"],
            "area": ["MINDSET", "LIFE", "RESULTS"],
            "result": ["RICH", "POWERFUL", "FOCUSED"]
        }

    # -------------------------------------

    def generate(self):

        pattern = random.choice(self.patterns)

        result = pattern

        for key in self.words:
            result = result.replace(
                "{" + key + "}",
                random.choice(self.words[key])
            )

        return result