import tkinter as tk
from tkinter import filedialog, simpledialog
import random

class LanguageQuizApp:
    def __init__(self, root):
        self.root = root
        root.title("Language Quiz")

        self.load_button = tk.Button(root, text="Load Files", command=self.load_files)
        self.load_button.pack()

        self.direction = tk.StringVar(value="ltr")
        self.direction_ltr_radio = tk.Radiobutton(root, text="Left to Right", variable=self.direction, value="ltr")
        self.direction_ltr_radio.pack()
        self.direction_rtl_radio = tk.Radiobutton(root, text="Right to Left", variable=self.direction, value="rtl")
        self.direction_rtl_radio.pack()

        self.start_button = tk.Button(root, text="Start Quiz", state=tk.DISABLED, command=self.start_quiz)
        self.start_button.pack()

        self.question_label = tk.Label(root, text="")
        self.question_label.pack()

        self.answer_entry = tk.Entry(root)
        self.answer_entry.pack()

        self.check_button = tk.Button(root, text="Check Answer", command=self.check_answer)
        self.check_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.score_label = tk.Label(root, text="Score: 0/0")
        self.score_label.pack()

        self.words = []
        self.current_word = None
        self.quiz_size = 0
        self.correct_answers = 0
        self.asked_questions = 0

        root.bind('<Return>', self.check_answer_wrapper)

    def load_files(self):
        file_paths = filedialog.askopenfilenames(title="Select Files", filetypes=[("Text files", "*.txt")])
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                lines = [line.strip().split(':') for line in file.readlines()]
                if self.direction.get() == "rtl":
                    lines = [line[::-1] for line in lines]  # Reverse word and translation
                self.words.extend(lines)

        if self.words:
            self.quiz_size = simpledialog.askinteger("Quiz Size", "How many words to quiz?", minvalue=1, maxvalue=len(self.words))
            self.start_button['state'] = tk.NORMAL

    def start_quiz(self):
        self.correct_answers = 0
        self.asked_questions = 0
        self.shuffled_words = random.sample(self.words, self.quiz_size)  # Shuffle and select quiz_size number of words
        self.update_score()
        self.ask_question()

    def ask_question(self):
        if self.asked_questions < self.quiz_size:
            self.current_word = self.shuffled_words[self.asked_questions]  # Pick the next word in the shuffled list
            self.question_label['text'] = f"What is the translation of '{self.current_word[0]}'?"
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus_set()
        else:
            self.finish_quiz()

    def check_answer(self, event=None):
        if self.asked_questions < self.quiz_size and self.current_word:
            user_answer = self.answer_entry.get()
            correct_answer = self.current_word[1]
            if user_answer.lower() == correct_answer.lower():
                self.correct_answers += 1
                self.result_label['text'] = "Correct!"
            else:
                self.result_label['text'] = f"Incorrect! The correct answer was '{correct_answer}'."
            self.asked_questions += 1
            self.update_score()
            if self.asked_questions < self.quiz_size:
                self.ask_question()

    def check_answer_wrapper(self, event):
        self.check_answer()

    def update_score(self):
        self.score_label['text'] = f"Score: {self.correct_answers}/{self.quiz_size}"

    def finish_quiz(self):
        self.question_label['text'] = "Quiz completed!"
        self.answer_entry['state'] = tk.DISABLED
        self.check_button['state'] = tk.DISABLED

root = tk.Tk()
app = LanguageQuizApp(root)
root.mainloop()
