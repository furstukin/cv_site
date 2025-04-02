import random

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import requests
from crossmorsepy import MorseAudio
from data import NATO_CODE, MORSE_CODE, BRAILLE, TRIVIA_CATEGORIES, TRIVIA_TYPE, TRIVIA_DIFFICULTY, TRIVIA_QUESTION_COUNT
from question_model import Question
from quiz_brain import QuizBrain
from quiz_ui import QuizInterface
from dotenv import load_dotenv
import os

load_dotenv()
morse_audio = MorseAudio()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CSRF_TOKEN')
Bootstrap4(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/morse', methods=['POST', 'GET'])
def morse():
    nato_sentence = ''
    morse_sentence = ''
    braille_sentence = ''
    if request.method == 'POST':
        text_to_convert = request.form.get('text-to-convert')
        morse_audio.play_audio(text_to_convert)
        nato_text = [NATO_CODE[letter] if letter.isalpha() else letter for letter in text_to_convert.upper()]
        morse_text = [MORSE_CODE[letter] for letter in text_to_convert.upper()]
        braille_text = [BRAILLE[letter] for letter in text_to_convert.lower()]
        nato_sentence = "NATO Phonetic: " + ' '.join(nato_text).strip()
        morse_sentence = "Morse Code: " + ''.join(morse_text).strip()
        braille_sentence = "Braille: " + ''.join(braille_text).strip()
    return render_template(
        'morse.html',
        nato_sentence=nato_sentence,
        morse_sentence=morse_sentence,
        braille_sentence=braille_sentence
    )

@app.route('/trivia', methods=['GET', 'POST'])
def trivia():
    if request.method == 'POST':
        category = TRIVIA_CATEGORIES[request.form['category']]
        question_count = request.form['question-count']
        difficulty = TRIVIA_DIFFICULTY[request.form['difficulty']]
        question_style = TRIVIA_TYPE[request.form['question-style']]
        quiz_parameters = {
            'amount': question_count,
            'category': category,
            'difficulty': difficulty,
            'type': question_style
        }

        quiz_data = requests.get(url="https://opentdb.com/api.php", params=quiz_parameters)
        quiz_data.raise_for_status()
        question_data = quiz_data.json()["results"]
        response = quiz_data.json()["response_code"]

        print(response)
        print(question_data)

        if response == 1:
            # Handle error
            flash("Error: The API couldn't provide enough questions for your query.", "danger")
            flash("Tip: Try reducing the number of questions or selecting a different category.", "danger")
        else:
        # Proceed with processing on success
            question_bank = []
            question_dict = {}
            index = 0
            for question in question_data:
                index += 1
                question_text = question["question"]
                correct_answer = question["correct_answer"]
                answers = question["incorrect_answers"] + [question["correct_answer"]]

                if question["type"] == 'multiple':
                    random.shuffle(answers)

                question_dict[f"Question {index} Text"] = question_text
                question_dict[f"Question {index} Answers"] = answers
                question_dict[f"Question {index} Correct"] = correct_answer
                new_question = Question(question_text, correct_answer)
                question_bank.append(new_question)
            flash("Your trivia game has been generated.")

            print(question_dict)

            # quiz = QuizBrain(question_bank)
            # game_interface = QuizInterface(quiz)
    return render_template('trivia.html', categories=TRIVIA_CATEGORIES, difficulties=TRIVIA_DIFFICULTY, type=TRIVIA_TYPE, q_count=TRIVIA_QUESTION_COUNT)

@app.route('/elements', methods=['GET', 'POST'])
def elements():
    return render_template('elements.html')

if __name__ == "__main__":
    app.run(debug=False, port=5002)