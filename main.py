from curriculum import SingleTypeCurriculumRandom, SingleTypeCurriculumByHistory
from session_manager import SessionManager
from questions import QuestionTypeBinaryOp

if __name__ == "__main__":
    question_type = QuestionTypeBinaryOp(min_a=2, max_a=5, min_b=2, max_b=10, op="*", random_swap=True)
    # curriculum = SingleTypeCurriculumRandom(question_type)
    curriculum = SingleTypeCurriculumByHistory(question_type)
    manager = SessionManager(curriculum, timeout=30)
    manager.study(10)
