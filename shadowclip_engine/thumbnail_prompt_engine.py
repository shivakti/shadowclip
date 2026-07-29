import random


def generate_thumbnail_prompt(hook):

    styles = [

        "youtube thumbnail dramatic lighting",
        "mrbeast style thumbnail",
        "high contrast viral thumbnail",
        "finance youtube thumbnail",
        "viral tiktok thumbnail"

    ]

    characters = [

        "serious man thinking",
        "shocked businessman",
        "man with mask mysterious",
        "person looking at money",
        "person surprised"

    ]

    style = random.choice(styles)
    character = random.choice(characters)

    prompt = f"{character}, {style}, big text saying '{hook}', cinematic lighting"

    return prompt