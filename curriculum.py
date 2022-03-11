import random
from questions import AbstractQuestionType, QuestionTypeBinaryOp, QuestionInstanceBinaryOp
from utils import choose_by_proportion

from HistoryLogger import HistoryLogger, ResponseRecord


class AbstractSingleTypeCurriculum:
    def __init__(self, **kargs):
        raise NotImplemented()

    def get_excercise(self):
        raise NotImplemented()

    def init_history(self, history: HistoryLogger):
        self.history = history


class SingleTypeCurriculumRandom(AbstractSingleTypeCurriculum):
    def __init__(self, question_type: AbstractQuestionType):
        self.all_questions = question_type.get_all()

    def get_excercise(self):
        all_questions_list = list(self.all_questions)
        selected_index = int(random.random() * len(all_questions_list))
        selected_question = all_questions_list[selected_index]
        return selected_question


class SingleTypeCurriculumByHistory(AbstractSingleTypeCurriculum):
    def __init__(self, question_type: AbstractQuestionType):
        self.question_type = question_type
        self.history = None  # use init_history()
        self.fallback_curriculum = SingleTypeCurriculumRandom(question_type)

    def update_history(self, rec: ResponseRecord):
        self.history.append(rec)

    def simple_priority_function(self, question):
        correct = self.history.get_question_correct_count(question)
        incorrect = self.history.get_question_incorrect_count(question)
        priority_score = max(incorrect - 0.5 * correct, 0)
        return priority_score

    def prioritize_exercises(self):
        candidate_questions = self.history.get_incorrect_questions()
        exercise_to_prio = {q: self.simple_priority_function(q) for q in candidate_questions}
        exercise_to_prio = {q: priority for (q, priority) in exercise_to_prio.items() if priority > 0}
        return exercise_to_prio

    def get_excercise(self):
        question_to_prio = self.prioritize_exercises()
        if len(question_to_prio) == 0:
            question = self.fallback_curriculum.get_excercise()
        else:
            ndx = choose_by_proportion(question_to_prio.values())
            question = list(question_to_prio.keys())[ndx]
        return question
