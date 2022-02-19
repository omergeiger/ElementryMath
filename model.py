import random

from typing import List

from color_print import colorprint, ColorCodes
from timed_input import input_answer, get_now
from questions import AbstractQuestionType, QuestionTypeBinaryOp, QuestionInstanceBinaryOp
from utils import choose_by_proportion

from HistoryLogger import HistoryLogger, ResponseRecord


class SingleTypeCurriculum:
    def __init__(self, question_type: AbstractQuestionType):
        self.all_questions = question_type.get_all()

    def get_random(self):
        all_questions_list = list(self.all_questions)
        selected_index = int(random.random() * len(all_questions_list))
        selected_question = all_questions_list[selected_index]
        return selected_question

    @staticmethod
    def simple_priority_function(question_history: List[ResponseRecord], eps=0):
        correct = len([rec for rec in question_history if rec.correct is True])
        incorrect = len(question_history) - correct
        priority_score = max(incorrect - 0.5 * correct, 0) + eps
        return priority_score

    # def prioritize_exercises(self, prioriry_func):
    #     exercise_to_prio = {(a, b): prioriry_func(correct, incorrect)
    #                         for ((a, b), (correct, incorrect)) in self.history.items()}
    #     exercise_to_prio = {(a, b): exercise_to_prio[(a, b)] for (a, b) in exercise_to_prio if
    #                         exercise_to_prio[(a, b)] > 0}
    #     return exercise_to_prio
    #
    # def generate_smart_exercise(self):
    #     if random.random() < self.random_portion:
    #         exercise = self.generate_random_exercise()
    #     else:
    #         exercise_to_prio = self.prioritize_exercises(Model.simple_priority_function)
    #
    #         # debug
    #         # print(sorted(exercise_to_prio.items(), key=lambda ((a, b), prio): prio, reverse=True))
    #
    #         ndx = choose_by_proportion(exercise_to_prio.values())
    #         if ndx is None:
    #             exercise = self.generate_random_exercise()
    #         else:
    #             (a, b) = list(exercise_to_prio.keys())[ndx]
    #             exercise = (a, b, a * b)
    #
    #     return exercise


class SessionManager:
    def __init__(self, curriculum: SingleTypeCurriculum, timeout=10):
        self.curriculum = curriculum
        self.timeout = timeout

    # def present(self, a, b, ans):
    #     print(get_now())
    #     print("{} * {} = ".format(a, b))
    #     user_answer = input_answer(self.timeout)
    #
    #     is_correct = (ans == user_answer)
    #     if is_correct:
    #         colorprint("YES :-)", ColorCodes.CORRECT)
    #     else:
    #         colorprint("NO :-(", ColorCodes.INCORRECT)
    #         colorprint("{} * {} = {}".format(a, b, ans), ColorCodes.INCORRECT)
    #     print("\n")
    #     return is_correct

    def present(self, question: QuestionInstanceBinaryOp):
        print(get_now())
        print(question)
        user_answer = input_answer(self.timeout)

        is_correct = (question.get_answer() == user_answer)
        if is_correct:
            colorprint("YES :-)", ColorCodes.CORRECT)
        else:
            colorprint("NO :-(", ColorCodes.INCORRECT)
            colorprint(f"{question}{question.get_answer()}", ColorCodes.INCORRECT)
        print("\n")
        return is_correct

    def study(self, num_exercises=5):
        for _ in range(num_exercises):
            # todo: self.generate_smart_exercise()
            question = self.curriculum.get_random()
            self.present(question)

            # is_correct = self.present(question)
            # current_counts = self.history[(a, b)]
            # if is_correct:
            #     current_counts = (current_counts[0] + 1, current_counts[1])
            # else:
            #     current_counts = (current_counts[0], current_counts[1] + 1)
            # self.history[(a, b)] = current_counts


class Model():
    def __init__(self, max_a=5, max_b=10, random_swap=True, random_portion=0.7, timeout=10):
        self.max_a = max_a
        self.max_b = max_b
        self.random_swap = random_swap
        self.random_portion = random_portion
        self.timeout = timeout
        self.max_num = max(max_a, max_b)
        self.history = {(a, b): (0, 0) for a in range(1, self.max_num + 1) for b in range(1, self.max_num + 1)}


if __name__ == "__main__":
    question_type = QuestionTypeBinaryOp(max_a=5, max_b=10, op="*", random_swap=True)
    curriculum = SingleTypeCurriculum(question_type)
    manager = SessionManager(curriculum)
    manager.study(5)
