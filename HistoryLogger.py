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
            self.history = []
        self.history.append(response_record)
