class ResponseRecord:
    def __init__(self, correct: bool, response: int, time):
        self.correct = correct
        self.response = response
        self.time = time


class HistoryLogger:
    def __init__(self):
        self.history = {}

    def log(self, question, response_record: ResponseRecord):
        if question not in self.history:
            self.history[question] = []
        self.history[question].append(response_record)

    def get_question_responses(self, question):
        if question not in self.history:
            return 0
        return len(self.history[question])

    def get_question_correct_count(self, question):
        if question not in self.history:
            return 0
        return len([rec for rec in self.history[question] if rec.correct is True])

    def get_question_incorrect_count(self, question):
        if question not in self.history:
            return 0
        return self.get_question_responses(question) - self.get_question_correct_count(question)

    def get_questions_in_history(self):
        return self.history.keys()

    def get_incorrect_questions(self):
        incorrect_questions = [q for q in self.history if self.get_question_incorrect_count(q) > 0]
        return incorrect_questions

    def count_correct_responses(self):
        questions = self.get_questions_in_history()
        total_correct = sum([self.get_question_correct_count(q) for q in questions])
        return total_correct

    def count_incorrect_responses(self):
        questions = self.get_questions_in_history()
        total_incorrect = sum([self.get_question_incorrect_count(q) for q in questions])
        return total_incorrect
