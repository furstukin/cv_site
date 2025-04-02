from data import TRIVIA_TYPE, TRIVIA_CATEGORIES, TRIVIA_DIFFICULTY
from question_model import Question
from quiz_brain import QuizBrain
from quiz_ui import QuizInterface
import requests
from bs4 import BeautifulSoup

quiz_parameters = {
    "amount": 10,
    "type": "boolean"
}

quiz_data = requests.get(url="https://opentdb.com/api.php", params=quiz_parameters)
quiz_data.raise_for_status()
question_data = quiz_data.json()["results"]

question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)
game_interface = QuizInterface(quiz)

# # Call API site and make soup
# response = requests.get("https://opentdb.com/api_config.php")
# response.raise_for_status()
#
# # Get the html back from the response
# site_html = response.text
#
# # Initialize BeautifulSoup on the html
# soup = BeautifulSoup(site_html, "html.parser")
#
# select_tag = soup.find('select', {'name': 'trivia_category'})
#
# # Extract values and categories
# categories = []
# for option in select_tag.find_all('option'):
#     value = option.get('value')
#     category = option.text
#     categories.append((value, category))
#
# # Print the result
# categories = {category:value for value, category in categories}
# print(categories)

