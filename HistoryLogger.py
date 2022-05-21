class ResponseRecord:
    def __init__(self, is_responded_and_correct: bool, response: int, time):
        self.is_responded_and_correct = is_responded_and_correct
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
        return len([rec for rec in self.history[question] if rec.is_responded_and_correct is True])

    def get_question_incorrect_count(self, question):
        if question not in self.history:
            return 0
        return len([rec for rec in self.history[question] if rec.is_responded_and_correct is False])

    def get_question_timedout_count(self, question):
        if question not in self.history:
            return 0
        return len([rec for rec in self.history[question] if rec.is_responded_and_correct is None])

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

    def count_timedout_responses(self):
        questions = self.get_questions_in_history()
        total_timedout= sum([self.get_question_timedout_count(q) for q in questions])
        return total_timedout
