from datetime import datetime
import signal


class TimeoutExcption(Exception):
    pass


def _interrupted(signum, frame):
    "called when read times out"
    raise TimeoutExcption()


signal.signal(signal.SIGALRM, _interrupted)


def _input_wrapper(timeout):
    signal.alarm(timeout)
    try:
        # python 2
        # input_str = raw_input()
        input_str = input()
        return input_str
    except:
        raise
    finally:
        signal.alarm(0)


def input_answer(timeout):
    try:
        in_string = _input_wrapper(timeout)
    except:
        print("timeout")
        return None

    try:
        input_int = int(in_string)
        return input_int
    except:
        print("invalid number")
        return None


def get_now():
    return datetime.now().strftime("%H:%M:%S")
