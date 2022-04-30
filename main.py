import curriculum
from session_manager import SessionManager

if __name__ == "__main__":
    manager = SessionManager(curriculum.curriculum_gilli_various_multiply, timeout=1000000)
    manager.study(num_exercises=3)
    manager.get_summary()
