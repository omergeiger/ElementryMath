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
        print()
        return None

    try:
        input_int = int(in_string)
        return input_int
    except:
        print("invalid number")
        return None
