from curriculum import *
from session_manager import SessionManager

# curriculum_nitzan2

if __name__ == "__main__":
    manager = SessionManager(curriculum_gilli_vertical_mult, timeout=1000000)
    manager.study(num_exercises=3)
    manager.get_summary()
