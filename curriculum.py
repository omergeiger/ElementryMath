from typing import List, Tuple

from questions import AbstractQuestionType, BinaryOperationQuestionType, BinaryOperationQuestion, MultitermAdditionQuestionType
from utils import choose_by_proportion

from HistoryLogger import HistoryLogger, ResponseRecord


class AbstractCurriculum:
    def __init__(self, **kargs):
        self.history = None
        raise NotImplemented()

    def get_question(self):
        raise NotImplemented()

    def init_history(self, history: HistoryLogger):
        self.history = history


class CurriculumRandom(AbstractCurriculum):
    def __init__(self, question_type: AbstractQuestionType):
        self.question_type = question_type

    def get_question(self):
        question = self.question_type.generate_question()
        return question


class CurriculumByErrors(AbstractCurriculum):
    def __init__(self, fallback_question_type: AbstractQuestionType):
        self.question_type = fallback_question_type
        self.fallback_curriculum = CurriculumRandom(fallback_question_type)

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

    def get_question(self):
        question_to_prio = self.prioritize_exercises()
        if len(question_to_prio) == 0:
            question = self.fallback_curriculum.get_question()
        else:
            ndx = choose_by_proportion(question_to_prio.values())
            question = list(question_to_prio.keys())[ndx]
        return question


class CompostiteCurriculum(AbstractCurriculum):
    def __init__(self, curriculum_proportions: List[Tuple[AbstractCurriculum, float]]):
        self.curriculums = [curriculum for (curriculum, proportion) in curriculum_proportions]
        self.proportions = [proportion for (curriculum, proportion) in curriculum_proportions]

    def get_question(self):
        curriculum_index = choose_by_proportion(self.proportions)
        curriculum = self.curriculums[curriculum_index]
        question = curriculum.get_question()
        return question

    def init_history(self, history: HistoryLogger):
        super().init_history(history)
        # common history for all sub-curriculums

        for curriculum in self.curriculums:
            curriculum.history = self.history


multiply_question_type = BinaryOperationQuestionType(min_a=2, max_a=5, min_b=2, max_b=10, op="*", random_swap=True)
add_question_type = BinaryOperationQuestionType(min_a=10, max_a=100, min_b=10, max_b=100, op="+", random_swap=True)
subtract_question_type = BinaryOperationQuestionType(min_a=10, max_a=100, min_b=10, max_b=100, op="-")
division_question_type = BinaryOperationQuestionType(min_a=2, max_a=100, min_b=2, max_b=10, op="/")

curriculum_gilli = CompostiteCurriculum(
    [
        (CurriculumRandom(question_type=multiply_question_type), 0.2),
        (CurriculumRandom(question_type=add_question_type), 0.2),
        (CurriculumRandom(question_type=subtract_question_type), 0.2),
        (CurriculumRandom(question_type=division_question_type), 0.2),
        (CurriculumByErrors(fallback_question_type=multiply_question_type), 0.2)
    ]
)

add_question_type_1 = BinaryOperationQuestionType(min_a=1, max_a=10, min_b=1, max_b=10, op="+", random_swap=True)
add_question_type_2 = BinaryOperationQuestionType(min_a=1, max_a=10, min_b=10, max_b=20, op="+", random_swap=True)
add_question_type_3 = BinaryOperationQuestionType(min_a=1, max_a=10, min_b=10, max_b=90, op="+", random_swap=True)
subtract_question_type = BinaryOperationQuestionType(min_a=1, max_a=10, min_b=1, max_b=10, op="-")

curriculum_nitzan = CompostiteCurriculum(
    [
        (CurriculumRandom(question_type=add_question_type_1), 0.4),
        (CurriculumRandom(question_type=add_question_type_2), 0.25),
        (CurriculumRandom(question_type=add_question_type_2), 0.15),
        (CurriculumRandom(question_type=subtract_question_type), 0.2),
    ]
)


multi_addition_question_type = MultitermAdditionQuestionType()

curriculum_nitzan_multiterm = CompostiteCurriculum(
    [
        (CurriculumRandom(question_type=multi_addition_question_type), 1.0),
    ]
)