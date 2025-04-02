from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"
FONT = ("Comic Sans MS", 18, "normal")
FONT1 = ("Comic Sans MS", 12, "normal")
RIGHT_COLOR = "green"
WRONG_COLOR = "red"
NORMAL_COLOR = "white"

class QuizInterface(Tk):
    def __init__(self, quiz_brain: QuizBrain):
        super().__init__()
        true_img = PhotoImage(file="static/images/true.png")
        false_img = PhotoImage(file="static/images/false.png")
        self.quiz = quiz_brain
        self.title("Trivia Night!")
        self.config(padx=20, pady=20, bg=THEME_COLOR)
        self.canvas = Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)
        self.question = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Test text",
            font=FONT,
            fill="black")
        self.score = Label(text=f"Score: {self.quiz.score}/{self.quiz.question_number}",
                           font=FONT1, bg=THEME_COLOR, highlightthickness=0)
        self.score.grid(column=1, row=0)
        self.true_btn = Button(image=true_img, highlightthickness=0, borderwidth=0,
                               relief="flat", command=self.check_true)
        self.true_btn.grid(column=0, row=2)
        self.false_btn = Button(image=false_img, highlightthickness=0, borderwidth=0,
                                relief="flat", command=self.check_false)
        self.false_btn.grid(column=1, row=2)
        self.get_next_question()

        self.mainloop()

    def get_next_question(self):
        self.canvas.config(bg=NORMAL_COLOR)
        if self.quiz.still_has_questions():
            self.score.config(text=f"Score: {self.quiz.score}/{self.quiz.question_number}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question, text=q_text)
        else:
            self.canvas.itemconfig(self.question, text=f"Your final score was: {self.quiz.score}/{self.quiz.question_number}")
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def check_true(self):
        result = self.quiz.check_answer("true")
        self.user_feedback(result)

    def check_false(self):
        result = self.quiz.check_answer("false")
        self.user_feedback(result)

    def user_feedback(self, is_right: bool):
        if is_right:
            self.canvas.config(bg=RIGHT_COLOR)
        else:
            self.canvas.config(bg=WRONG_COLOR)
        self.after(1000, self.get_next_question)