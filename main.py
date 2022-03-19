import curriculum
from session_manager import SessionManager
from questions import BinaryOperationQuestionType

if __name__ == "__main__":
    manager = SessionManager(curriculum.curriculum_nitzan_multiterm, timeout=30)
    manager.study(num_exercises=10)
