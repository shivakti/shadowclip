import random

VIRAL_PATTERNS = [

"THIS CHANGES EVERYTHING",
"NOBODY TALKS ABOUT THIS",
"YOU NEED TO HEAR THIS",
"THE TRUTH ABOUT MONEY",
"THIS WILL SHOCK YOU",
"THIS IS WHY YOU FAIL",
"STOP DOING THIS",
"THIS IS THE REAL GAME",
"THIS WILL CHANGE YOUR LIFE",
"THIS IS WHY YOU'RE BROKE"

]

def generate_hook(transcript: str):

    words = transcript.split()

    if len(words) > 6:
        hook = " ".join(words[:6]).upper()
        return hook

    return random.choice(VIRAL_PATTERNS)


def generate_thumbnail_text(hook: str):

    words = hook.split()

    if len(words) > 4:
        return " ".join(words[:4])

    return hook