import tkinter as tk
import csv
import os


class TestApp():
    def __init__(self, filename) -> None:
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.root.title("Test App")
        self.filename = filename
        self.question = tk.Label(self.root, text='')
        self.selected_answer = tk.StringVar(value=None)
        self.score = 0
        self.number_of_wrong_answers = 0

        # Use Radiobuttons in a group
        self.radiobutton1 = tk.Radiobutton(self.root, variable=self.selected_answer, value="1")
        self.radiobutton2 = tk.Radiobutton(self.root, variable=self.selected_answer, value="2")
        self.radiobutton3 = tk.Radiobutton(self.root, variable=self.selected_answer, value="3")
        self.radiobutton4 = tk.Radiobutton(self.root, variable=self.selected_answer, value="4")

        
        self.question.grid(row=0, column=0, columnspan=4, pady=5)
        self.radiobutton1.grid(row=1, column=1, sticky='W', pady=(0, 0))
        self.radiobutton2.grid(row=1, column=2, sticky='W', pady=(0, 0))
        self.radiobutton3.grid(row=2, column=1, sticky='W', pady=(0, 0))
        self.radiobutton4.grid(row=2, column=2, sticky='W', pady=(0, 0))

        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

        self.next_button = tk.Button(self.root, text='Submit', command=self.nextquestion)
        self.next_button.grid(row=3, column=0, columnspan=4, pady=20)

        self.score_label = tk.Label(self.root, text=f'Score = {self.score}')
        self.score_label.grid(row=1, column=3)

        self.question_number = 0
        self.questions = []
        self.current_index = 0
        self.test_over = False

        self.run()

    def update_score_label(self):
        self.score_label.config(text=f'Score = {self.score}')

    def disable_radio_buttons(self):
            self.radiobutton1.config(state=tk.DISABLED)
            self.radiobutton2.config(state=tk.DISABLED)
            self.radiobutton3.config(state=tk.DISABLED)
            self.radiobutton4.config(state=tk.DISABLED)
    

    def test_end(self):
        if self.question_number >= 10 and self.number_of_wrong_answers >= 5:
            self.question.config(text="You've Failed")
            self.test_over = True
        elif self.question_number >= 10 and self.score >= 7:
            self.question.config(text="You've Passed! Good Job!")
            self.test_over = True

        if self.test_over:
            self.disable_radio_buttons()

    def read_csv(self):
        try:
            file_path = os.path.abspath(self.filename)
            print("Absolute path:", file_path)
            with open(file_path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    self.questions.append(row)

        except Exception as e:
            error_message = f"Error loading the file: {str(e)}"
            print(error_message)

    def checkanswer(self):
        selected_answer_value = self.selected_answer.get()
        correct_answer = self.questions[self.current_index][5]
        print(f'Correct answer is: {correct_answer}')
        if selected_answer_value != correct_answer:
            self.number_of_wrong_answers += 1
        else:
            self.score += 1
        print(f"Selected option: {selected_answer_value}")

    def nextquestion(self):
        self.checkanswer()
        self.question_number += 1
        self.current_index = (self.current_index + 1) % len(self.questions)
        self.question.config(text=self.questions[self.current_index][0])
        self.radiobutton1.config(text=self.questions[self.current_index][1])
        self.radiobutton2.config(text=self.questions[self.current_index][2])
        self.radiobutton3.config(text=self.questions[self.current_index][3])
        self.radiobutton4.config(text=self.questions[self.current_index][4])
        self.selected_answer.set(None)
        self.update_score_label()
        self.test_end()
        if self.test_over:
            self.next_button.config(state=tk.DISABLED)

    def run(self):
        self.read_csv()
        if not self.test_over:
            self.nextquestion()
        self.root.mainloop()


if __name__ == '__main__':
    filename = 'MCQAnswers.csv'
    app = TestApp(filename)