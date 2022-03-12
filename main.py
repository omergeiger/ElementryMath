import curriculum
from session_manager import SessionManager
from questions import QuestionTypeBinaryOp

if __name__ == "__main__":
    manager = SessionManager(curriculum.curriculum_gilli, timeout=30)
    manager.study(num_exercises=10)
