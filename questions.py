import random


class AbstractQuestionType:
    def __init__(self, **kargs):
        raise NotImplemented()

    def generate_question(self):
        raise NotImplemented()


class BinaryOperationQuestionType(AbstractQuestionType):
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

        elif self.op in {'-', '/'}:
            # make a1 smaller
            if (a1 < b1):
                a1, b1 = b1, a1

            if self.op == '/':
                # force whole devision
                a1 = int(a1 / b1) * b1

        return a1, b1

    def generate_question(self):
        a1, b1 = self._generate_question_args()
        a1, b1 = self._fix_question_args_by_op(a1, b1)
        question = BinaryOperationQuestion(a1, b1, self.op)
        return question


class MultitermAdditionQuestionType(AbstractQuestionType):
    def __init__(self, min_term_count=2, max_term_count=3, min_term_value=1, max_term_value=20,
                 min_result=11, max_result=20, swap=True):
        self.min_term_count = min_term_count
        self.max_term_count = max_term_count
        self.min_term_value = min_term_value
        self.max_term_value = max_term_value
        self.min_result = min_result
        self.max_result = max_result
        self.shuffle = swap

        self._assert_feasibility()

    def _assert_feasibility(self):
        assert (self.max_result / self.min_term_count <= self.max_term_value)
        assert (self.min_result / self.max_term_count >= self.min_term_value)

    def _get_feasable_term_range(self, remaining_term_count, remaining_result):
        min_val = max(remaining_result - (remaining_term_count - 1) * self.max_term_value, self.min_term_value)
        max_val = min(remaining_result - (remaining_term_count - 1) * self.min_term_value, self.max_term_value)
        return (min_val, max_val)

    def _generate_question_args(self):
        terms = []
        num_terms = random.randint(self.min_term_count, self.max_term_count)
        remaining_result = random.randint(self.min_result, self.max_result)

        for _ in range(num_terms):
            min_val, max_val = self._get_feasable_term_range(remaining_term_count=num_terms - len(terms),
                                                             remaining_result=remaining_result)
            new_term = random.randint(min_val, max_val)
            terms.append(new_term)
            remaining_result -= new_term

        if self.shuffle:
            random.shuffle(terms)

        return terms

    def generate_question(self):
        terms = self._generate_question_args()
        question = MultitermOperationQuestion(terms, "+")
        return question


class AbstractQuestionInstance:
    def get_answer(self) -> int:
        raise NotImplemented()


class BinaryOperationQuestion(AbstractQuestionInstance):
    def __init__(self, a, b, op="*"):
        self.a = a
        self.b = b

        assert (op in ["*", "+", "-", "/"])
        self.op = op
        self.answer = eval(self.as_expression())

    def as_expression(self):
        return f"{self.a} {self.op} {self.b}"

    def get_answer(self):
        return self.answer

    def __repr__(self):
        return f"{self.as_expression()} = "


class MultitermOperationQuestion(AbstractQuestionInstance):
    def __init__(self, terms, op="+"):
        self.terms = terms

        assert (op in ["*", "+", "-", "/"])
        self.op = op
        self.answer = eval(self.as_expression())

    def as_expression(self):
        return f" {self.op} ".join(map(str, self.terms))

    def get_answer(self):
        return self.answer

    def __repr__(self):
        return f"{self.as_expression()} = "
