import requests
import html
import random

from unicodedata import category


class QuizCall:
    def __init__(self, q_count, q_category, difficulty, q_style):
        self.q_count = q_count
        self.category = q_category
        self.difficulty = difficulty
        self.q_style = q_style

    def api_call(self):
        # API request for trivia questions
        if self.category != 'any':
            quiz_parameters = {
                'amount': self.q_count,
                'category': self.category,
                'difficulty': self.difficulty,
                'type': self.q_style
            }
        else:
            quiz_parameters = {
                'amount': self.q_count,
                'difficulty': self.difficulty,
                'type': self.q_style
            }

        quiz_data = requests.get(url="https://opentdb.com/api.php", params=quiz_parameters)
        quiz_data.raise_for_status()
        question_data = quiz_data.json()["results"]
        response_code = quiz_data.json()["response_code"]

        # Check API response and handle errors
        if response_code == 1:
            return "Response 1"

        # Dynamically create question_dict
        grouped_questions = []  # Create a list to store grouped question dictionaries
        index = 0

        for question in question_data:
            index += 1
            question_text = html.unescape(question["question"])
            correct_answer = html.unescape(question["correct_answer"])
            answers = [html.unescape(answer) for answer in question["incorrect_answers"] + [question["correct_answer"]]]

            # Shuffle answers for multiple-choice questions, sort for Boolean questions
            if question["type"] == 'multiple':
                random.shuffle(answers)
            else:
                answers = sorted(answers, reverse=True)

            # Create a dictionary for the current question and add it to the list
            grouped_questions.append({
                "index": index,  # Question number
                "text": question_text,
                "answers": answers,
                "correct": correct_answer
            })

        return grouped_questions
