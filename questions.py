import random


class AbstractQuestionType:
    def __init__(self, **kargs):
        raise NotImplemented()

    def generate_question(self):
        raise NotImplemented()


class QuestionTypeBinaryOp(AbstractQuestionType):
    def __init__(self, min_a=1, max_a=5, min_b=1, max_b=10, op="*", random_swap=True):
        self.min_a = min_a
        self.max_a = max_a
        self.min_b = min_b
        self.max_b = max_b

        assert (op in ["*", "+", "-", "/"])
        self.op = op
        self.swap = random_swap

    def _generate_question_args(self):
        a1 = int(self.min_a + random.random() * (self.max_a + 1 - self.min_a))
        b1 = int(self.min_b + random.random() * (self.max_b + 1 - self.min_b))
        return a1, b1

    def _fix_question_args_by_op(self, a1, b1):
        if self.op in {"*", "+"}:
            if self.swap is True and random.random() < 0.5:
                a1, b1 = b1, a1

        elif self.op in  {'-', '/'}:
            # make a1 smaller
            if (a1 < b1):
                a1, b1 = b1, a1

            if self.op == '/':
                # force whole devision
                a1 = int(a1/b1) * b1

        return a1, b1

    def generate_question(self):
        a1, b1 = self._generate_question_args()
        a1, b1 = self._fix_question_args_by_op(a1, b1)
        question = QuestionInstanceBinaryOp(a1, b1, self.op)
        return question


class AbstractQuestionInstance:
    def get_answer(self) -> int:
        raise NotImplemented()


class QuestionInstanceBinaryOp(AbstractQuestionInstance):
    def __init__(self, a, b, op="*"):
        self.a = a
        self.b = b

        assert (op in ["*", "+", "-", "/"])
        self.op = op
        self.answer = eval(f"a {op} b")

    def get_answer(self):
        return self.answer

    def __repr__(self):
        return f"{self.a} {self.op} {self.b} = "
