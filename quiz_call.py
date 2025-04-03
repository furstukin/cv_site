import requests
import html
import random

class QuizCall:
    def __init__(self, question_count, category, difficulty, question_style):
        self.question_count = question_count
        self.category = category
        self.difficulty = difficulty
        self.question_style = question_style

    def api_call(self):
        # API request for trivia questions
        quiz_parameters = {
            'amount': self.question_count,
            'category': self.category,
            'difficulty': self.difficulty,
            'type': self.question_style
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
