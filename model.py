import random

from timed_input import input_answer, get_now
from color_print import colorprint, ColorCodes
from utils import choose_by_proportion


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
                (a, b) = list(exercise_to_prio.keys())[ndx]
                exercise = (a, b, a * b)

        return exercise

    def present(self, a, b, ans):
        print(get_now())
        print("{} * {} = ".format(a, b))
        user_answer = input_answer(self.timeout)

        is_correct = (ans == user_answer)
        if is_correct:
            colorprint("YES :-)", ColorCodes.CORRECT)
        else:
            colorprint("NO :-(", ColorCodes.INCORRECT)
            colorprint("{} * {} = {}".format(a, b, ans), ColorCodes.INCORRECT)
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
