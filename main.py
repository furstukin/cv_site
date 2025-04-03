import random
import html
from flask import Flask, render_template, redirect, url_for, request, flash, session
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
    return render_template('trivia.html', categories=TRIVIA_CATEGORIES, difficulties=TRIVIA_DIFFICULTY, type=TRIVIA_TYPE, q_count=TRIVIA_QUESTION_COUNT)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Get parameters for API call
        category = TRIVIA_CATEGORIES[request.form['category']]
        question_count = request.form['question-count']
        difficulty = TRIVIA_DIFFICULTY[request.form['difficulty']]
        question_style = TRIVIA_TYPE[request.form['question-style']]

        # API request for trivia questions
        quiz_parameters = {
            'amount': question_count,
            'category': category,
            'difficulty': difficulty,
            'type': question_style
        }
        quiz_data = requests.get(url="https://opentdb.com/api.php", params=quiz_parameters)
        quiz_data.raise_for_status()
        question_data = quiz_data.json()["results"]
        response_code = quiz_data.json()["response_code"]

        # Check API response and handle errors
        if response_code == 1:
            flash("Error: The API couldn't provide enough questions for your query.", "danger")
            flash("Tip: Try reducing the number of questions or selecting a different category.", "danger")
            return redirect(url_for('trivia'))

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

        # Store the question dictionary in the session
        session['grouped_questions'] = grouped_questions
        session['trivia_form_submitted'] = True  # Set the flag
        flash("Your trivia quiz has been generated. Good luck!", "info")

        # Pass question_dict to the template
        return render_template('quiz.html', grouped_questions=grouped_questions)

    elif request.method == 'GET':
        # Check if the form has been submitted, otherwise redirect
        if not session.get('trivia_form_submitted'):
            flash("You must complete the trivia setup first!", "danger")
            return redirect(url_for('trivia'))

# For testing only
@app.route('/elements', methods=['GET', 'POST'])
def elements():
    return render_template('elements.html')

if __name__ == "__main__":
    app.run(debug=False, port=5002)