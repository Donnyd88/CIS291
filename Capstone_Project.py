import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import os
from pathlib import Path
from tkinter import PhotoImage


class TestApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.root.title("Test App")
        script_dir = Path(__file__).parent  # Get the directory of the current script
        file_path = script_dir / 'mccLogo.png'
        icon = PhotoImage(file=file_path)
        self.root.iconphoto(False, icon)
        self.filename = None
        self.text = False

        self.num_of_test_questions = 0

        # Initialize educator_frame 
        self.educator_frame = None

        self.read_config_file_percents()

        # Welcome Page
        self.show_welcome_page()

        self.root.mainloop()


    def read_config_file_percents(self):
        try:
            with open('config.csv', 'r') as file:
                reader = csv.reader(file)
                self.quick_pass_percentage, self.fail_percentage, self.end_question_num = next(reader)
        
        except FileNotFoundError:
            self.fail_percentage = 69
            self.quick_pass_percentage = 90
            self.end_question_num = 15


    def show_welcome_page(self):
        if self.educator_frame:
            self.educator_frame.destroy()
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(fill='both', expand=True)

        welcome_label = tk.Label(self.welcome_frame, text="Welcome to the Test App!", font=('Helvetica', 20))
        welcome_label.pack(pady=20)

        # Student ID Entry
        student_id_label = tk.Label(self.welcome_frame, text="Enter Student ID:")
        student_id_label.pack(pady=5)
        self.student_id_entry = tk.Entry(self.welcome_frame)
        self.student_id_entry.pack(pady=5)

        educator_button = tk.Button(self.welcome_frame, text= "For Educators", command = self.for_educators_page)
        educator_button.pack(pady=10)

        start_button = tk.Button(self.welcome_frame, text="Start Test", command=self.start_test)
        start_button.pack(pady=10)


    def for_educators_page(self):
        self.welcome_frame.destroy()
        self.educator_frame = tk.Frame(self.root)
        self.educator_frame.pack(fill="both", expand=True)

        welcome_teachers_label = tk.Label(self.educator_frame, text = "Welcome Educators!", font=('Helvetica', 20))
        welcome_teachers_label.pack(pady=10)

        pass_percent_label = tk.Label(self.educator_frame, text="Enter the Quick Pass Percentage:")
        pass_percent_label.pack(pady=5)

        self.pass_percent_entry = tk.Entry(self.educator_frame)
        self.pass_percent_entry.pack(pady=5)

        fail_percent_label = tk.Label(self.educator_frame, text ="Enter the Quick Fail Percentage:")
        fail_percent_label.pack(pady=5)

        self.fail_percent_entry = tk.Entry(self.educator_frame)
        self.fail_percent_entry.pack(pady=5)
        
        check_test_end_label = tk.Label(self.educator_frame, text = "What question number should the Quick Pass or Quick fail activete on?")
        check_test_end_label.pack(pady=5)

        self.check_test_end_entry = tk.Entry(self.educator_frame)
        self.check_test_end_entry.pack(pady=5)

        back_button = tk.Button(self.educator_frame, text = "Back", command = self.show_welcome_page)
        back_button.pack(pady=10)
       
        def save_variables():

            # Get the values from the Entry widgets
            pass_percent = self.pass_percent_entry.get()
            fail_percent = self.fail_percent_entry.get()
            test_end_num = self.check_test_end_entry.get()

            try:
                # Open the CSV file in read mode
                with open('config.csv', 'r', newline='') as file:
                    # Create a CSV reader object
                    reader = csv.reader(file)
                    # Read the existing values from the CSV file
                    existing_values = next(reader, [])
            except FileNotFoundError:
                # If the file doesn't exist, create a new file with default values
                existing_values = [90, 69, 15]
                with open('config.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(existing_values)

            try:
                # Update the existing values with the new values from the Entry widgets
                if pass_percent:
                    existing_values[0] = pass_percent
                if fail_percent:
                    existing_values[1] = fail_percent
                if test_end_num:
                    existing_values[2] = test_end_num
            except IndexError:
                # If there are not enough elements in existing_values, extend it with None values
                while len(existing_values) < 3:
                    existing_values.append(None)
                # Update the existing values again
                if pass_percent:
                    existing_values[0] = pass_percent
                if fail_percent:
                    existing_values[1] = fail_percent
                if test_end_num:
                    existing_values[2] = test_end_num

            # Open the CSV file in write mode
            with open('config.csv', 'w', newline='') as file:
                # Create a CSV writer object
                writer = csv.writer(file)
                # Write the updated values to the CSV file
                writer.writerow(existing_values)

        save_button = tk.Button(self.educator_frame, text = "Save", command = save_variables)
        save_button.pack(pady=10)


    def start_test(self):
        # Destroy the welcome frame and start the test
        self.welcome_frame.destroy()

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Select File", command=self.select_file)
        self.file_menu.add_separator()  # Add a separator
        self.file_menu.add_command(label="Quit", command=self.quit_application) 


        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about_popup)

        # Dropdown menu for file selection
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

        # Create and hide text entry
        self.text_entry = tk.Entry(self.root)
        self.text_entry.grid(row=4, column=0, columnspan=4, pady=10)
        self.text_entry.grid_forget()  # Hide the text entry initially

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

    def quit_application(self):
        self.root.quit()

    def show_about_popup(self):
        about_text = "This is a simple quiz application.\nCreated by Donald Deal."
        tk.messagebox.showinfo("About", about_text)


    def select_file(self):
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File",
                                                   filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if self.filename:
            self.read_csv()
            self.nextquestion()

    def calculate_score(self):
        if self.score > 0:
            last_question_number = self.question_number - 1
            prec_correct = round((self.score / last_question_number) * 100, 2)
            return prec_correct
        else:
            return self.score

    def update_score_label(self):
        if self.score > 0:
            percentage_score = self.calculate_score()
            self.score_label.config(text=f'Score = {percentage_score}%')
            if percentage_score > 79:
                self.score_label.config(fg='green')
            elif percentage_score > 70:
                self.score_label.config(fg="orange")
            else:
                self.score_label.config(fg="red")
        else:
            self.score_label.config(text=f'Score = {self.score}')

    def disable_radio_buttons(self):
        self.radiobutton1.config(state=tk.DISABLED)
        self.radiobutton2.config(state=tk.DISABLED)
        self.radiobutton3.config(state=tk.DISABLED)
        self.radiobutton4.config(state=tk.DISABLED)


    def enable_radio_buttons(self):
        self.radiobutton1.config(state=tk.NORMAL)
        self.radiobutton2.config(state=tk.NORMAL)
        self.radiobutton3.config(state=tk.NORMAL)
        self.radiobutton4.config(state=tk.NORMAL)

    def hide_radio_buttons(self):
        if hasattr(self, 'radio_buttons'):
            for button in self.radio_buttons:
                button.config(state=tk.HIDDEN)

    def show_radio_buttons(self):
        if hasattr(self, 'radio_buttons'):
            for button in self.radio_buttons:
                button.config(state=tk.NORMAL)

    def hide_text_entry(self):
        # Hide the text entry
        self.text_entry.grid_remove()

    def show_text_entry(self):
        # Show the text entry
        self.text_entry.grid(row=3, column=0, columnspan=4, pady=10)


    def test_end(self):
        score = self.calculate_score()
        if self.question_number >= int(self.end_question_num) and score <= int(self.fail_percentage):
            self.question.config(text="You've Failed.")
            self.test_over = True
        elif self.question_number >= int(self.end_question_num) and score >= int(self.quick_pass_percentage):
            self.question.config(text="You've Passed! Good Job!")
            self.test_over = True
        elif self.question_number == (int(self.num_of_test_questions) - 1):
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
                    self.num_of_test_questions += 1
        except Exception as e:
            error_message = f"Error loading the file: {str(e)}"
            print(error_message)

    def checkanswer(self):
        text_answer = self.text_entry.get().strip().lower()
        correct_answer = self.questions[self.current_index][5].strip().lower()
        selected_answer_value = self.selected_answer.get()
        
        if self.text:
            if text_answer == correct_answer:
                self.score += 1
                print("You were right! TEXT")
            else:
                print("TEXT ANSWER incorrect!")
                self.number_of_wrong_answers += 1
        else:
            if selected_answer_value == correct_answer:
                self.score += 1
                print("You were right! MULTIPLE CHOICE")
            else:
                print("incorrect! MULTIPLE CHOICE")
                self.number_of_wrong_answers += 1

        print(f'Correct answer is: {correct_answer}')
        print(f"Inputted Text: {text_answer}")
        if not self.text:  # Only print selected option for multiple-choice questions
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

        question_type = self.questions[self.current_index][-1]
        print(f"question type: {question_type}")
        self.text = False
        if question_type == "text":
            self.text = True
            self.disable_radio_buttons()
            self.show_text_entry()
            self.selected_answer.set(None)  # Reset selected_answer variable to None for text questions
            # Move the Submit button to a different row
            self.next_button.grid(row=5, column=0, columnspan=4, pady=20)
        else:
            self.hide_text_entry()
            self.enable_radio_buttons()
            self.selected_answer.set(None)  # Reset selected_answer variable to None for text questions
            # Move the Submit button back to row 3
            self.next_button.grid(row=3, column=0, columnspan=4, pady=20)

        self.update_score_label()
        self.test_end()
        if self.test_over:
            self.next_button.config(state=tk.DISABLED)



if __name__ == '__main__':
    app = TestApp()
