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

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    if request.method == 'POST':
        # Get parameters for API call
        category = TRIVIA_CATEGORIES[request.form['category']]
        question_count = request.form['question-count']
        difficulty = TRIVIA_DIFFICULTY[request.form['difficulty']]
        question_style = TRIVIA_TYPE[request.form['question-style']]
        quiz_call = QuizCall(question_count, category, difficulty, question_style)
        api_call = quiz_call.api_call()

        # Check response and return error if response is 1
        if api_call == "Response 1":
            flash("Error: The API couldn't provide enough questions for your query.", "danger")
            flash("Tip: Try reducing the number of questions or selecting a different category.", "danger")
            return redirect(url_for('trivia'))

        # Create question_dict
        grouped_questions = api_call  # Create a list to store grouped question dictionaries
        index = 0

        quiz_brain = QuizBrain(grouped_questions)

        # Serialize QuizBrain attributes
        session['quiz_brain'] = quiz_brain.serialize()

        flash("Your trivia quiz has been generated. Good luck!", "info")
        return redirect(url_for('quiz', first_load=True))


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Ensure QuizBrain exists in session
    if 'quiz_brain' not in session:
        flash("You must complete the trivia setup first!", "danger")
        return redirect(url_for('trivia'))

    # Deserialize QuizBrain from session ONCE
    quiz_brain_data = session.get('quiz_brain')
    quiz_brain = QuizBrain.deserialize(quiz_brain_data)

    feedback = None
    if request.method == 'POST':
        # Process user answer
        user_answer = request.form.get('user_answer')  # Get user's answer
        feedback = quiz_brain.check_answer(user_answer)  # Check answer
        flash(f"{feedback} Your score is {quiz_brain.score}/{quiz_brain.question_number}", "success")
        # Save updated state to session
        session['quiz_brain'] = quiz_brain.serialize()  # Ensure changes are saved

        # Redirect if quiz is over
        if not quiz_brain.still_has_questions():
            flash(f"Your final score was: {quiz_brain.score}/{quiz_brain.question_number}", "success")
            return redirect(url_for('trivia'))

    # Get the next question
    current_question = quiz_brain.next_question()
    session['quiz_brain'] = quiz_brain.serialize()  # Save updated state to session

    return render_template(
        'quiz.html',
        current_question=current_question,
        answers=quiz_brain.current_question['answers'],
        feedback=feedback
    )


# For testing only
@app.route('/elements', methods=['GET', 'POST'])
def elements():
    return render_template('elements.html')

if __name__ == "__main__":
    app.run(debug=False, port=5002)