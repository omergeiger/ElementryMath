from color_print import colorprint, ColorCodes
from timed_input import input_answer
from utils import get_now
from questions import AbstractQuestionType, BinaryOperationQuestionType, BinaryOperationQuestion
from curriculum import AbstractCurriculum
from utils import get_epoch

from HistoryLogger import HistoryLogger, ResponseRecord


class SessionManager:
    def __init__(self, curriculum: AbstractCurriculum, timeout=10):
        self.timeout = timeout
        self.history = HistoryLogger()
        self.curriculum = curriculum
        self.curriculum.init_history(self.history)

    def present_question(self, question: BinaryOperationQuestion):
        print(get_now())
        print(question)
        start = get_epoch()
        response = input_answer(self.timeout)
        end = get_epoch()
        time_elapsed = end - start
        return response, time_elapsed

    def present_response(self, question, correct):
        if correct:
            colorprint("YES :-)", ColorCodes.CORRECT)
        else:
            colorprint("NO :-(", ColorCodes.INCORRECT)
            colorprint(f"{question}{question.get_answer()}", ColorCodes.INCORRECT)
        print("\n")

    def study(self, num_exercises=5):
        for _ in range(num_exercises):
            question = self.curriculum.get_question()
            (response, time) = self.present_question(question)
            is_correct = (question.get_answer() == response)
            self.present_response(question, is_correct)
            response_record = ResponseRecord(is_correct, response, time)
            self.history.log(question, response_record)
