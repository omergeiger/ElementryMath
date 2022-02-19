import random


def choose_by_proportion(proportions):
    sum_all = sum(proportions)
    if len(proportions) == 0 or sum_all == 0:
        return None

    normalized_proportions = [p / sum_all for p in proportions]

    # debug
    # print(normalized_proportions)

    length = len(normalized_proportions)
    cdf = [sum(normalized_proportions[:i + 1]) for i in range(length)]

    random_num = random.random()

    for i in range(length):
        if cdf[i] >= random_num:
            return i

    return length - 1
