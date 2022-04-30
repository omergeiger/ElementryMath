from datetime import datetime
from enum import Enum

import time
import random


def choose_by_proportion(proportions):
    sum_all = sum(proportions)
    if len(proportions) == 0 or sum_all == 0:
        return None

    normalized_proportions = [p / sum_all for p in proportions]

    length = len(normalized_proportions)
    cdf = [sum(normalized_proportions[:i + 1]) for i in range(length)]

    random_num = random.random()

    for i in range(length):
        if cdf[i] >= random_num:
            return i

    return length - 1


def get_now():
    return datetime.now().strftime("%H:%M:%S")


def get_epoch():
    return int(time.time())


class ColorCodes(Enum):
    CORRECT = '\033[92m'
    INCORRECT = '\033[91m'


class ResponseStrings:
    POSITIVE = "YES :-)"
    NEGATIVE = "NO :-("


def colorprint(text: str, color_code: ColorCodes):
    ENDC = '\033[0m'
    print(color_code.value + text + ENDC)
