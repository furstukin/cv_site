import random
import html
from flask import Flask, render_template, redirect, url_for, request, flash, session, get_flashed_messages
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from crossmorsepy import MorseAudio
from data import NATO_CODE, MORSE_CODE, BRAILLE, TRIVIA_CATEGORIES, TRIVIA_TYPE, TRIVIA_DIFFICULTY, TRIVIA_QUESTION_COUNT
from quiz_brain import QuizBrain
from dotenv import load_dotenv
import os
from quiz_call import QuizCall
from contact_manager import ContactManager
from eeg_rfc_class import EegEyeModel
from home_price_ann_class import HousePriceModel

load_dotenv()

MY_EMAIL = os.getenv('MY_EMAIL')
MY_EMAIL2 = os.getenv('MY_EMAIL2')
contact_manager = ContactManager()
morse_audio = MorseAudio()
eeg_eye_model = EegEyeModel()
hpm = HousePriceModel()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('CSRF_TOKEN')
Bootstrap5(app)

@app.route("/", methods=['GET', 'POST'])
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
        if request.form['category'] == "":
            q_category = 'any'
        else:
            q_category = TRIVIA_CATEGORIES[request.form['category']]
        if request.form['question-count'] == "":
            question_count = 10
        else:
            question_count = request.form['question-count']
        difficulty = TRIVIA_DIFFICULTY[request.form['difficulty']]
        question_style = TRIVIA_TYPE[request.form['question-style']]
        quiz_call = QuizCall(q_count=question_count, q_category=q_category, difficulty=difficulty, q_style=question_style)
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

    anchor = ""
    feedback = None
    is_post = False
    if request.method == 'POST':
        anchor = 'question'
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
        feedback=feedback,
        anchor=anchor,
        is_post=is_post
    )

@app.route('/resume', methods=['GET', 'POST'])
def resume():
    return render_template('resume.html')

@app.route('/mindreader', methods=['GET', 'POST'])
def mind_reader():
    eye_state = ""
    if request.method == 'POST':
        af3 = float(request.form.get('af3'))
        f7 = float(request.form.get('f7'))
        f3 = float(request.form.get('f3'))
        fc5 = float(request.form.get('fc5'))
        t7 = float(request.form.get('t7'))
        p = float(request.form.get('p'))
        o1 = float(request.form.get('o1'))
        o2 = float(request.form.get('o2'))
        p8 = float(request.form.get('p8'))
        t8 = float(request.form.get('t8'))
        fc6 = float(request.form.get('fc6'))
        f4 = float(request.form.get('f4'))
        f8 = float(request.form.get('f8'))
        af4 = float(request.form.get('af4'))

        brain_wave = [[af3*1000, f7*1000, f3*1000, fc5*1000, t7*1000, p*1000, o1*1000, o2*1000, p8*1000, t8*1000, fc6*1000, f4*1000, f8*1000, af4*1000]]
        prediction = eeg_eye_model.predict(brain_wave)
        if prediction[0] == 1:
            eye_state = 'open'
        else:
            eye_state = 'closed'

    return render_template('mindreader.html', eye_state=eye_state)

@app.route('/homeprices', methods=['GET', 'POST'])
def home_prices():
    home_val = ""
    if request.method == 'POST':
        sqft = float(request.form.get('sqft'))
        n_bed = float(request.form.get('n-bed'))
        n_bath = float(request.form.get('n-bath'))
        low_fl = float(request.form.get('low-fl'))
        y_blt = float(request.form.get('y-blt'))
        lot_sz = float(request.form.get('lot-sz'))
        gr_sz = float(request.form.get('gr-sz'))
        nb_ql = float(request.form.get('nb-ql'))

        home_attr = [[sqft, n_bed, n_bath, low_fl, y_blt, lot_sz, gr_sz, nb_ql]]
        prediction = hpm.predict(home_attr)
        home_val = f"${prediction[0][0]:,.2f}"

    return render_template('homeprices.html', home_val=home_val)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        from_email = request.form.get('email')
        body = request.form.get('message')

        # Create message container
        msg = MIMEMultipart("alternative")
        msg['From'] = MY_EMAIL
        msg['To'] = from_email
        msg['Subject'] = f"You have a new contact message on your CV Site from {name}"

        # Initialize the email body
        email_body = []

        full_email_body = ("<html><body><p>" + f"Hello Dustin, <br><br>Here is the contact message from:<br><br>"
                                               f"{name}<br>"
                                               f"{from_email}<br>"
                           + "".join(email_body)
                           + f"{body}</p></body></html>")
        msg.attach(MIMEText(full_email_body, "html"))
        message = msg.as_string()
        contact_manager.send_email(from_email=MY_EMAIL, user_email=MY_EMAIL2, message=message)
        flash('Your message was sent.', 'success')  # Make sure this is called
        return redirect(url_for('home'))  # Ensure the redirect aligns with the `home` route

# For testing only
@app.route('/elements', methods=['GET', 'POST'])
def elements():
    return render_template('elements.html')

if __name__ == "__main__":
    app.run(debug=False, port=5002)