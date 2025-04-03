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
from dotenv import load_dotenv
import os
from quiz_call import QuizCall

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
        quiz_call = QuizCall(category, question_count, difficulty, question_style)
        api_call = quiz_call.api_call()

        # Check response and return error if response is 1
        if api_call == "Response 1":
            flash("Error: The API couldn't provide enough questions for your query.", "danger")
            flash("Tip: Try reducing the number of questions or selecting a different category.", "danger")
            return redirect(url_for('trivia'))

        # Create question_dict
        grouped_questions = api_call  # Create a list to store grouped question dictionaries
        index = 0

        # Set session value to ensure form was submitted
        session['trivia_form_submitted'] = True  # Set the flag
        flash("Your trivia quiz has been generated. Good luck!", "info")

        #  Add a loop to send one question at a time to the html
        #  Update quiz.html to remove for loops? may not be needed...
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