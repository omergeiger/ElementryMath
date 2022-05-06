from datetime import datetime
from enum import Enum
from math import ceil, log10

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


class Range:
    def __init__(self, low, hi):
        self.low = low
        self.hi = hi


def digits2range(num_digits):
    low = 10 ** (num_digits - 1) if num_digits > 1 else 1
    hi = 10 ** num_digits - 1
    return Range(low, hi)


def num2digits(num):
    if num <= 0:
        raise Exception(f"bad arg num2digits({num}). negative num")
    if num == 1:
        return 1
    return ceil(log10(num) + 0.0001)

# sanity test for num2digits()
# for i in [0.0001,1,5,9,10,11,99,100,101]:
#     print(f"{i} {num2digits(i)}")
