import random

FINANCE_HOOKS = [

"THIS WILL MAKE YOU RICH",
"STOP BEING BROKE",
"THIS IS WHY YOU HAVE NO MONEY",
"THE MONEY SECRET",
"THE TRUTH ABOUT MONEY",
"HOW RICH PEOPLE THINK",
"THIS CHANGES YOUR FINANCES",
"YOU NEED TO HEAR THIS"

]

FACE_HOOKS = [

"LISTEN TO THIS",
"THIS IS IMPORTANT",
"THIS CHANGES EVERYTHING",
"NOBODY TALKS ABOUT THIS",
"PAY ATTENTION"

]


def generate_hook(transcript, video_type):

    if video_type == "face":

        return random.choice(FACE_HOOKS)

    if video_type == "slides":

        return random.choice(FINANCE_HOOKS)

    return "WATCH THIS"