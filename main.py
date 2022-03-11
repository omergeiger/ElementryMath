from curriculum import CurriculumRandom, CurriculumByErrors, CompostiteCurriculum
from session_manager import SessionManager
from questions import QuestionTypeBinaryOp

if __name__ == "__main__":
    multiply_question_type = QuestionTypeBinaryOp(min_a=2, max_a=5, min_b=2, max_b=10, op="*", random_swap=True)
    add_question_type = QuestionTypeBinaryOp(min_a=10, max_a=100, min_b=10, max_b=100, op="+", random_swap=True)
    subtract_question_type = QuestionTypeBinaryOp(min_a=10, max_a=100, min_b=10, max_b=100, op="-")
    division_question_type = QuestionTypeBinaryOp(min_a=2, max_a=100, min_b=2, max_b=10, op="/")

    curriculum = CompostiteCurriculum(
        [
            (CurriculumRandom(question_type=multiply_question_type), 0.2),
            (CurriculumRandom(question_type=add_question_type), 0.2),
            (CurriculumRandom(question_type=subtract_question_type), 0.2),
            (CurriculumRandom(question_type=division_question_type), 0.2),
            (CurriculumByErrors(fallback_question_type=multiply_question_type), 0.2)
        ]
    )
    manager = SessionManager(curriculum, timeout=30)
    manager.study(10)
