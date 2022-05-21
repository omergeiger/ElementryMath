from curriculum import *
from session_manager import SessionManager

# curriculum_gilli_vertical_mult

if __name__ == "__main__":
    manager = SessionManager(curriculum_gilli_various_multiply, timeout=30)
    manager.study(num_exercises=10)
    manager.get_summary()
