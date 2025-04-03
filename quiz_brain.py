import html

class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None
        self.answers = []

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        if self.still_has_questions():
            self.current_question = self.question_list[self.question_number]
            self.question_number += 1
            q_text = html.unescape(self.current_question['text'])
            self.answers = self.current_question['answers']
            return f"Q.{self.question_number}: {q_text}"
        else:
            print(f"Your final score was: {self.score}/{self.question_number}")

    def check_answer(self, user_answer):
        correct_answer = html.unescape(self.current_question['correct'])
        if user_answer[0].lower() == correct_answer[0].lower():
            self.score += 1
            # print("You got it right!")
            # return True
            print(f"Score: {self.score}")
            return "You got it right!"
        else:
            # print(f"That's wrong. It is actually {correct_answer}")
            # return False
            return f"That's wrong. It is actually {correct_answer}"

    # def answer_list(self):
    #     self.answers = self.current_question['answers']
    #     for answer in self.answers:
    #         print(answer)

    # def get_next_question(self):
    #     if self.still_has_questions():
    #         print(f"Score: {self.score}/{self.question_number}")
    #         self.next_question()
    #         # self.answer_list()
    #     else:
    #         print(f"Your final score was: {self.score}/{self.question_number}")

    def serialize(self):
        print(f"DEBUG: Serializing QuizBrain with score: {self.score}")
        return {
            'question_number': self.question_number,
            'score': self.score,
            'question_list': self.question_list,
            'current_question': self.current_question
        }

    @staticmethod
    def deserialize(data):
        print(f"DEBUG: Deserializing QuizBrain with score: {data.get('score')}")
        qb = QuizBrain(data['question_list'])
        qb.question_number = data['question_number']
        qb.score = data['score']
        qb.current_question = data['current_question']
        return qb




