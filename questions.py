class AbstractQuestionType:
    def __init__(self, **kargs):
        raise NotImplemented()

    def get_all(self):
        pass


class QuestionTypeBinaryOp(AbstractQuestionType):
    def __init__(self, min_a=1, max_a=5, min_b=1, max_b=10, op="*", random_swap=True):
        self.min_a = min_a
        self.max_a = max_a
        self.min_b = min_b
        self.max_b = max_b

        assert (op in ["*", "+", "-", "/"])
        self.op = op
        self.swap = random_swap
        self.all_questions = self._generate_all()

    def _generate_all(self):
        all_questions = {QuestionInstanceBinaryOp(a, b, self.op) for a in range(self.min_a, self.max_a + 1) for b in
                         range(self.min_b, self.max_b + 1)}
        if self.swap is True:
            swapped = {QuestionInstanceBinaryOp(a, b, self.op) for a in range(self.min_b, self.max_b + 1) for b in
                       range(self.min_a, self.max_a + 1)}
            all_questions = all_questions.union(swapped)
        return all_questions

    def get_all(self):
        return self.all_questions


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
