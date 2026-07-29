import random


class HookLibrary:

    def __init__(self):

        self.hooks = [

            "THIS WILL CHANGE YOUR LIFE",
            "THE TRUTH ABOUT SUCCESS",
            "YOU ARE NOT READY FOR THIS",
            "WHY MOST PEOPLE FAIL",
            "THIS CHANGES EVERYTHING",
            "THE SECRET NOBODY TELLS YOU",
            "THIS WILL BLOW YOUR MIND",
            "YOU NEED TO SEE THIS",
            "THIS IS NEXT LEVEL",
            "THE TRUTH ABOUT MONEY",
            "MOST PEOPLE DON'T KNOW THIS",
            "THIS IS PURE GENIUS",
            "WATCH THIS CAREFULLY",
            "THIS WILL SURPRISE YOU",
            "THE SYSTEM HIDES THIS",
            "THIS IDEA IS POWERFUL",
            "THIS IS THE REALITY",
            "THIS WILL OPEN YOUR MIND",
            "THIS CHANGES HOW YOU THINK",
            "THE POWER OF DISCIPLINE"

        ]

    def random_hook(self):

        return random.choice(self.hooks)