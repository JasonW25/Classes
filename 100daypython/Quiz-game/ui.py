import tkinter as tk
from typing import Text
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class UserInterface():

    def __init__(self, quiz_brain: QuizBrain):
        self.score = 0

        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quiz Game")
        self.window.config(pady=20, padx=20, bg=THEME_COLOR)

        self.score_text = tk.Label(text="Score: 0", fg="white", bg=THEME_COLOR, font=("ariel", 10, "normal"))
        self.score_text.grid(column=1, row=0)

        self.canvas = tk.Canvas(height=500, width=600, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)
        self.question_text = self.canvas.create_text(300, 250, width=480, text="test", fill="black", font=("ariel", 15, "normal"))

        self.true_image = tk.PhotoImage(file="images/true.png")
        self.true_button = tk.Button(image=self.true_image, command=self.press_true)
        self.true_button.grid(row=3, column=1)

        self.false_image = tk.PhotoImage(file="images/false.png")
        self.false_button = tk.Button(image=self.false_image, command=self.press_false)
        self.false_button.grid(row=3, column=0)
        
        self.get_next_q()

        self.window.mainloop()

    def get_next_q(self):
        self.canvas.config(bg="white")
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)
        if q_text == f"The quiz is over. Your score is {self.score}":
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def press_true(self):
        self.feedback(self.quiz.check_answer("True"))

    def press_false(self):
        self.feedback(self.quiz.check_answer("False"))

    def feedback(self, grade):
        if grade == True:
            self.score += 1
            self.score_text.config(text=f"Score: {self.score}")
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(500, self.get_next_q)

