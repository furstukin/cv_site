import html

class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question['text'])
        print(f"Q.{self.question_number}: {q_text}")
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        correct_answer = html.unescape(self.current_question['correct'])
        if user_answer[0].lower() == correct_answer[0].lower():
            self.score += 1
            print("You got it right!")
            return True
        else:
            print(f"That's wrong. It is actually {correct_answer}")
            return False

    def answer_list(self):
        answers = self.current_question['answers']
        for answer in answers:
            print(answer)

    def get_next_question(self):
        if self.still_has_questions():
            print(f"Score: {self.score}/{self.question_number}")
            self.next_question()
            self.answer_list()
        else:
            print(f"Your final score was: {self.score}/{self.question_number}")


