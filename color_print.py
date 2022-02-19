from enum import Enum


class ColorCodes(Enum):
    CORRECT = '\033[92m'
    INCORRECT = '\033[91m'


def colorprint(text: str, color_code: ColorCodes):
    ENDC = '\033[0m'
    print(color_code.value + text + ENDC)
