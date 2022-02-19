import random
from datetime import datetime
import signal

eps = 0.001


class TimeoutExcption(Exception):
    pass


def interrupted(signum, frame):
    "called when read times out"
    raise TimeoutExcption()


signal.signal(signal.SIGALRM, interrupted)


def input(timeout):
    signal.alarm(timeout)
    try:
        input_str = raw_input()
        return input_str
    except:
        raise
    finally:
        signal.alarm(0)


def input_answer(timeout):
    try:
        in_string = input(timeout)
    except:
        print("timeout")
        return None

    try:
        input_int = int(in_string)
        return input_int
    except:
        print("invalid number")
        return None


def get_now():
    return datetime.now().strftime("%H:%M:%S")


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


class ColorPrint:
    CORRECT = '\033[92m'
    INCORRECT = '\033[91m'
    ENDC = '\033[0m'

    # HEADER = '\033[95m'
    # OKBLUE = '\033[94m'
    # OKCYAN = '\033[96m'
    # OKGREEN = '\033[92m'
    # WARNING = '\033[93m'
    # FAIL = '\033[91m'
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'

    @staticmethod
    def colorprint(text, color):
        print(color + text + ColorPrint.ENDC)


#################

class Model():
    def __init__(self, max_a=5, max_b=10, random_swap=True, random_portion=0.7, timeout=10):
        self.max_a = max_a
        self.max_b = max_b
        self.random_swap = random_swap
        self.random_portion = random_portion
        self.timeout = timeout
        self.max_num = max(max_a, max_b)
        self.history = {(a, b): (0, 0) for a in range(1, self.max_num + 1) for b in range(1, self.max_num + 1)}

    def generate_random_exercise(self):
        a = 1 + int(random.random() * self.max_a)
        b = 1 + int(random.random() * self.max_b)
        if self.random_swap and random.random() > 0.5:
            a, b = b, a
        return (a, b, a * b)

    @staticmethod
    def simple_priority_function(correct, incorrect, eps=0):
        priority_score = max(incorrect - 0.5 * correct, 0) + eps
        return priority_score

    def prioritize_exercises(self, prioriry_func):
        exercise_to_prio = {(a, b): prioriry_func(correct, incorrect)
                            for ((a, b), (correct, incorrect)) in self.history.items()}
        exercise_to_prio = {(a, b): exercise_to_prio[(a, b)] for (a, b) in exercise_to_prio if
                            exercise_to_prio[(a, b)] > 0}
        return exercise_to_prio

    def generate_smart_exercise(self):
        if random.random() < self.random_portion:
            exercise = self.generate_random_exercise()
        else:
            exercise_to_prio = self.prioritize_exercises(Model.simple_priority_function)

            # debug
            # print(sorted(exercise_to_prio.items(), key=lambda ((a, b), prio): prio, reverse=True))

            ndx = choose_by_proportion(exercise_to_prio.values())
            if ndx is None:
                exercise = self.generate_random_exercise()
            else:
                (a, b) = exercise_to_prio.keys()[ndx]
                exercise = (a, b, a * b)

        return exercise

    def present(self, a, b, ans):
        print(get_now())
        print("{} * {} = ".format(a, b))
        user_answer = input_answer(self.timeout)

        is_correct = (ans == user_answer)
        if is_correct:
            ColorPrint.colorprint("YES :-)", ColorPrint.CORRECT)
        else:
            ColorPrint.colorprint("NO :-(", ColorPrint.INCORRECT)
            ColorPrint.colorprint("{} * {} = {}".format(a, b, ans), ColorPrint.INCORRECT)
        print("\n")
        return is_correct

    def study(self, num_exercises=5):
        for _ in range(num_exercises):
            a, b, ans = self.generate_smart_exercise()
            is_correct = self.present(a, b, ans)
            current_counts = self.history[(a, b)]
            if is_correct:
                current_counts = (current_counts[0] + 1, current_counts[1])
            else:
                current_counts = (current_counts[0], current_counts[1] + 1)
            self.history[(a, b)] = current_counts


if __name__ == '__main__':
    model = Model(max_a=5, max_b=10, random_swap=True, random_portion=0.75, timeout=25)
    model.study(num_exercises=10)

    # debug
    # print(sorted(model.history.items(), key=lambda ((a, b), (c, i)): (i, c), reverse=True))
