from utils import colorprint, ColorCodes, ResponseStrings
from timed_input import input_answer
from utils import get_now, sleep_between_questions
from questions import BinaryOperationQuestion
from curriculum import AbstractCurriculum
from utils import get_epoch

from HistoryLogger import HistoryLogger, ResponseRecord


class SessionSummary:
    def __init__(self, total_score, passed, correct_count, incorrect_count, timedout_count):
        self.total_score = total_score
        self.passed = passed
        self.correct_count = correct_count
        self.incorrect_count = incorrect_count
        self.timedout_count = timedout_count

    def present(self):
        summary_string = f"SUMMARY {ResponseStrings.POSITIVE if self.passed else ResponseStrings.NEGATIVE}   SCORE {self.total_score}"
        summary_color = ColorCodes.CORRECT if self.passed else ColorCodes.INCORRECT

        print("*" * len(summary_string))
        colorprint(summary_string, summary_color)
        print("*" * len(summary_string))

        colorprint(f"{ResponseStrings.POSITIVE} : {self.correct_count}", ColorCodes.CORRECT)
        colorprint(f"{ResponseStrings.NEGATIVE} : {self.incorrect_count}", ColorCodes.INCORRECT)
        colorprint(f"{ResponseStrings.TIMEOUT} : {self.timedout_count}", ColorCodes.TIMEOUT)

        print("*" * len(summary_string))


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

    def present_response(self, question, is_responded_and_correct, time):
        if is_responded_and_correct is True:
            colorprint(ResponseStrings.POSITIVE, ColorCodes.CORRECT)
        elif is_responded_and_correct is False:
            colorprint(ResponseStrings.NEGATIVE, ColorCodes.INCORRECT)
            colorprint(f"{question}{question.get_answer()}", ColorCodes.INCORRECT)
        elif is_responded_and_correct is None:
            colorprint(ResponseStrings.TIMEOUT, ColorCodes.TIMEOUT)
            colorprint(f"{question}{question.get_answer()}", ColorCodes.TIMEOUT)

        print(f"response time: {time}")
        print()

    def study(self, num_exercises=5):
        for _ in range(num_exercises):
            sleep_between_questions()
            question = self.curriculum.get_question()
            (response, time) = self.present_question(question)
            is_responded_and_correct = (question.get_answer() == response) if response is not None else None
            self.present_response(question, is_responded_and_correct, time)
            response_record = ResponseRecord(is_responded_and_correct, response, time)
            self.history.log(question, response_record)

    def get_summary(self, present=True, score_threshold=50, count_timoutout_as_incorrect=False):
        history = self.curriculum.history
        incorrect_count = history.count_incorrect_responses()
        correct_count = history.count_correct_responses()
        timedout_count = history.count_timedout_responses()
        if count_timoutout_as_incorrect is True:
            total_score = round(100 * correct_count / (correct_count + incorrect_count + timedout_count))
        elif count_timoutout_as_incorrect is False:
            total_score = round(100 * correct_count / (correct_count + incorrect_count))
        passed = total_score >= score_threshold

        session_summary = SessionSummary(total_score, passed, correct_count, incorrect_count, timedout_count)
        if present:
            session_summary.present()

        return session_summary
