from hook_library import HookLibrary
import random


class ViralHookGenerator:

    def __init__(self):

        self.library = HookLibrary()

    def generate(self, transcript):

        base_hook = self.library.random_hook()

        return base_hook