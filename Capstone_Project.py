import tkinter as tk
import sys
from tkinter import ttk, filedialog, messagebox 
import csv
import os
from tkinter import PhotoImage
import logging
from PIL import Image, ImageTk
import bcrypt
from tkinter.font import Font


class TestApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x800")
        alabaster = "#F1F4FF"
        silver = "#A2A2A1"
        blue = "#4267B2"
        light_grey = "#F1F3F4"
        self.bg_color = blue
        self.fg_color = light_grey
        self.root.configure(bg=self.bg_color) 
        self.root.title("Test App")
        self.custom_font = Font(family="Lato", size=15)
        self.title_font = Font(family="Lato", size=20, weight="bold", slant="italic", underline=1)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'mccLogo.ico')
        ico_image = Image.open(file_path)
        if hasattr(sys, '_MEIPASS'):
            file_path = os.path.join(sys._MEIPASS, 'mccLogo.ico')
        else:
            file_path = 'mccLogo.ico'
        icon = ImageTk.PhotoImage(ico_image)
        self.root.iconphoto(False, icon)
        script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.filename = os.path.join(script_dir, 'MCQAnswersPlusText.csv')
        self.text = False
        self.student_id = None 
        self.correct_password = "password"
        self.error = False
        

        self.num_of_test_questions = 0

        # Initialize educator_frame 
        self.educator_frame = None

        # Initialize CSV file path
        self.csv_file_path = "test_scores.csv"

        # Check if the CSV file exists
        if not os.path.isfile(self.csv_file_path):
            # If the file doesn't exist, create it and write headers
            self.write_csv_headers()

        self.read_config_file_percents()


        # Welcome Page
        self.show_welcome_page()

        self.root.mainloop()

    def hash_password(self, password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def check_password_with_hash(self, plain_password, hashed_password):
        # Ensure plain_password is encoded as bytes
        plain_password_bytes = plain_password.encode('utf-8')

        return bcrypt.checkpw(plain_password_bytes, hashed_password)

       



    def write_csv_headers(self):
        # Define the headers
        headers = ["Student ID", "Score"]
        
        # Open the CSV file in write mode
        with open(self.csv_file_path, 'w', newline='') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile)
            
            # Write the headers to the CSV file
            csv_writer.writerow(headers)

    def read_config_file_percents(self):
        try:
            with open('config.csv', 'r') as file:
                reader = csv.reader(file)
                self.quick_pass_percentage, self.fail_percentage, self.end_question_num, hashed_password = next(reader)
                self.correct_password = hashed_password.encode('utf-8')
           
                
            self.quick_pass_percentage = int(self.quick_pass_percentage)
            self.fail_percentage = int(self.fail_percentage)
            self.end_question_num = int(self.end_question_num)
            
        except FileNotFoundError:
            # If the file doesn't exist, create a new file with default values
            self.correct_password = self.hash_password(self.correct_password)
            existing_values = [90, 69, 15, self.correct_password.decode('utf-8')]
            with open('config.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(existing_values)

    def can_start_test(self):
        # Get the entered student ID
        student_id = self.student_id_entry.get()

        if student_id.strip() == "":
            # If the student ID entry is empty, display an error message
            self.error_label.config(text="Please enter a student ID.")
        else:
            self.error_label.config(text="")  # Clear the error message
            self.start_test()

    def show_welcome_page(self):
        if self.educator_frame:
            self.educator_frame.destroy()
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.configure(bg=self.bg_color)
        self.welcome_frame.pack(fill='both', expand=True)

        welcome_label = tk.Label(self.welcome_frame, text="Welcome to the Test App!", font= self.title_font, foreground=self.fg_color,  background=self.bg_color)
        welcome_label.pack(pady=20)

        # Student ID Entry
        student_id_label = tk.Label(self.welcome_frame, text="Enter Student ID or Name:")
        student_id_label.place(relx=0.5, rely=0.45, anchor="center")
        student_id_label.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        self.student_id_entry = tk.Entry(self.welcome_frame)
        self.student_id_entry.configure(bg="white", font= self.custom_font)
        self.student_id_entry.place(relx=0.5, rely=0.5, anchor="center")

        button_frame = tk.Frame(self.welcome_frame)
        button_frame.pack(side="bottom", pady=(0, 100))
        button_frame.configure(bg=self.bg_color)

        self.error_label = tk.Label(self.welcome_frame,  fg="red", font=self.custom_font, text="")
        self.error_label.configure(bg=self.bg_color)
        self.error_label.pack(side="bottom", padx=10, pady=10)

        educator_button = tk.Button(button_frame, text="For Educators", command=self.for_educators_page)
        educator_button.configure(bg=self.bg_color, font= self.custom_font, fg=self.fg_color)
        educator_button.pack(side="left", padx=10, pady=10)

    
        start_button = tk.Button(button_frame, text="Start Test", command=self.can_start_test)
        start_button.configure(bg=self.bg_color, font= self.custom_font, fg=self.fg_color)
        start_button.pack(side="left", padx=10, pady=10)

    def for_educators_page(self):
        # Destroy the existing frames
        if self.educator_frame:
            self.educator_frame.destroy()
        if self.welcome_frame:
            self.welcome_frame.destroy()

        # Create the educator frame
        self.educator_frame = tk.Frame(self.root)
        self.educator_frame.configure(bg=self.bg_color)
        self.educator_frame.pack(fill="both", expand=True)

        # Password Entry
        password_label = tk.Label(self.educator_frame, text="Enter password:")
        password_label.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        password_label.place(relx=0.5, rely=0.45, anchor="center")
        self.password_entry = tk.Entry(self.educator_frame, show="*")  # Show asterisks for password input
        self.password_entry.configure(bg="white", font= self.custom_font)
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        # Button to submit password
        submit_button = tk.Button(self.educator_frame, text="Submit", command=self.check_password)
        submit_button.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        submit_button.place(relx=0.55, rely=0.6, anchor="center")

        back_button = tk.Button(self.educator_frame, text="Back", command=self.show_welcome_page)
        back_button.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        back_button.place(relx=0.45, rely=0.6, anchor="center")

    def check_password(self):
        # Get the entered password
        entered_password = self.password_entry.get()

        
        if  self.check_password_with_hash(entered_password, self.correct_password):

            self.show_educator_page()
        else:
            messagebox.showerror("Error", "Incorrect password. Please try again.")

    def show_educator_page(self):
        if self.educator_frame:
            self.educator_frame.destroy()
        self.educator_frame = tk.Frame(self.root)
        self.educator_frame.configure(bg=self.bg_color)
        self.educator_frame.pack(fill="both", expand=True)

        welcome_teachers_label = tk.Label(self.educator_frame, text = "Welcome Educators!", font=self.custom_font, foreground=self.fg_color,  background=self.bg_color, borderwidth=1, highlightthickness=1)
        welcome_teachers_label.pack(pady=20)

        pass_percent_label = tk.Label(self.educator_frame, text="Enter the Quick Pass Percentage:")
        pass_percent_label.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        pass_percent_label.pack(pady=5)

        self.pass_percent_entry = tk.Entry(self.educator_frame)
        self.pass_percent_entry.configure(foreground=self.fg_color, font= self.custom_font,  background="white")
        self.pass_percent_entry.pack(pady=5)

        fail_percent_label = tk.Label(self.educator_frame, text ="Enter the Quick Fail Percentage:")
        fail_percent_label.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        fail_percent_label.pack(pady=5)

        self.fail_percent_entry = tk.Entry(self.educator_frame)
        self.fail_percent_entry.configure(foreground=self.fg_color, font= self.custom_font,  background="white")
        self.fail_percent_entry.pack(pady=5)
        
        check_test_end_label = tk.Label(self.educator_frame, text = "What question number should the Quick Pass or Quick fail activete on?")
        check_test_end_label.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        check_test_end_label.pack(pady=5)

        self.check_test_end_entry = tk.Entry(self.educator_frame)
        self.check_test_end_entry.configure(foreground=self.fg_color, font= self.custom_font,  background="white")
        self.check_test_end_entry.pack(pady=5)

        update_password_label = tk.Label(self.educator_frame, text = "Enter new password:")
        update_password_label.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        update_password_label.pack(pady=5)

        self.update_password_entry = tk.Entry(self.educator_frame, show = "*")
        self.update_password_entry.configure(foreground=self.fg_color, font= self.custom_font,  background="white")
        self.update_password_entry.pack(pady=5)


        self.verify_update_password_label = tk.Label(self.educator_frame, text = "Re-enter new password:")
        self.verify_update_password_label.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        self.verify_update_password_label.pack(pady=5)

        self.verify_update_password_entry = tk.Entry(self.educator_frame, show = "*")
        self.verify_update_password_entry.configure(foreground=self.fg_color, font= self.custom_font,  background="white")
        self.verify_update_password_entry.pack(pady=5)

        self.apply_outcome_label = tk.Label(self.educator_frame, text = "")
        self.apply_outcome_label.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        self.apply_outcome_label.pack(pady=5)

        button_frame = tk.Frame(self.educator_frame)
        button_frame.configure(bg=self.bg_color)
        button_frame.pack(side="bottom", pady=(0, 100))

        back_button = tk.Button(button_frame, text = "Back", command = self.show_welcome_page)
        back_button.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        back_button.pack(side="left", padx=10, pady=10)


        
        def save_variables():
            # Get the values from the Entry widgets
            pass_percent_str = self.pass_percent_entry.get()
            fail_percent_str = self.fail_percent_entry.get()
            test_end_num_str = self.check_test_end_entry.get()
            update_password = self.update_password_entry.get()
            verify_update_password = self.verify_update_password_entry.get()

            # Validate and update pass_percent if it's not empty
            if pass_percent_str:
                try:
                    pass_percent = int(pass_percent_str)
                except ValueError:
                    self.apply_outcome_label.config(text="Invalid input for pass percentage")
                    return
            else:
                pass_percent = None

            # Validate and update fail_percent if it's not empty
            if fail_percent_str:
                try:
                    fail_percent = int(fail_percent_str)
                except ValueError:
                    self.apply_outcome_label.config(text="Invalid input for fail percentage")
                    return
            else:
                fail_percent = None

            # Validate and update test_end_num if it's not empty
            if test_end_num_str:
                try:
                    test_end_num = int(test_end_num_str)
                except ValueError:
                    self.apply_outcome_label.config(text="Invalid input for test end number")
                    return
            else:
                test_end_num = None

            if update_password and verify_update_password and update_password != verify_update_password:
                self.apply_outcome_label.config(text="Passwords do not match")
                return

         

            existing_values = [90, 69, 15, "password"]

            # Update the existing values with the new values from the Entry widgets
            if pass_percent is not None:
                existing_values[0] = pass_percent
            if fail_percent is not None:
                existing_values[1] = fail_percent
            if test_end_num is not None:
                existing_values[2] = test_end_num
            if update_password and verify_update_password and (update_password == verify_update_password):
                # Hash the new password
                update_password = self.hash_password(update_password).decode('utf-8')
                existing_values[3] = update_password
            else:
                self.apply_outcome_label.config(text="Passwords do not match")
                return  # Return from the function if passwords don't match


            # Write the updated values back to the CSV file
            with open('config.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(existing_values)
                print(existing_values)
                self.apply_outcome_label.config(text="Settings have been updated successfully! Restart for new password to take effect.")


        save_button = tk.Button(button_frame, text = "Save", command = save_variables)
        save_button.configure(foreground=self.fg_color, font= self.custom_font,  background=self.bg_color)
        save_button.pack(side="left", padx=10, pady=10)



    def is_valid_student_id(self):
        self.student_id = self.student_id_entry.get()
        if self.student_id.strip() == "":
            self.error_text = "Please enter your student ID."
        return self.student_id.strip() != ""
    
    def start_test(self):

        self.student_id = self.student_id_entry.get()
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
        self.question.config(bg=self.bg_color, font=self.custom_font, fg=self.fg_color)
        self.selected_answer = tk.StringVar(value=None)
        self.score = 0
        self.number_of_wrong_answers = 0

        # Use Radiobuttons in a group
        self.radiobutton1 = ttk.Radiobutton(self.root, variable=self.selected_answer, value="1")
        self.radiobutton2 = ttk.Radiobutton(self.root, variable=self.selected_answer, value="2")
        self.radiobutton3 = ttk.Radiobutton(self.root, variable=self.selected_answer, value="3")
        self.radiobutton4 = ttk.Radiobutton(self.root, variable=self.selected_answer, value="4")
        radiobuttons_list = [self.radiobutton1, self.radiobutton2, self.radiobutton3, self.radiobutton4]

        style = ttk.Style()
        style.map("Custom.TRadiobutton",
                  foreground=[('selected', 'black')]) 
        style.configure("Custom.TRadiobutton", background=self.bg_color, font=self.custom_font, foreground=self.fg_color)

        for radio_button in radiobuttons_list:
            radio_button.configure(style="Custom.TRadiobutton")

        
       # for radio_button in radiobuttons_list:
            #radio_button.config(style="TRadiobutton", bg=self.bg_color, font=self.custom_font, foreground=self.fg_color, activebackground=self.fg_color, activeforeground=self.bg_color)


        self.question.grid(row=0, column=0, columnspan=4, pady=5)
        self.radiobutton1.grid(row=1, column=1, sticky='W', pady=(0, 0))
        self.radiobutton2.grid(row=1, column=2, sticky='W', pady=(0, 0))
        self.radiobutton3.grid(row=2, column=1, sticky='W', pady=(0, 0))
        self.radiobutton4.grid(row=2, column=2, sticky='W', pady=(0, 0))

        # Create and hide text entry
        self.text_entry = tk.Entry(self.root)
        self.text_entry.configure(font=self.custom_font)
        self.text_entry.grid(row=4, column=0, columnspan=4, pady=10)
        self.text_entry.grid_forget()  # Hide the text entry initially

        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

        self.next_button = tk.Button(self.root, text='Submit', command=self.nextquestion)
        self.next_button.config(bg=self.bg_color, font=self.custom_font, fg=self.fg_color)
        self.next_button.grid(row=3, column=0, columnspan=4, pady=20)

        self.score_label = tk.Label(self.root, text=f'Score = {self.score}')
        self.score_label.configure(bg=self.bg_color, font=self.custom_font, fg=self.fg_color)
        self.score_label.grid(row=1, column=3)

        self.question_number = 0
        self.questions = []
        self.current_index = 0
        self.test_over = False
        self.read_csv()
        self.nextquestion()

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
            self.score_label.config(text=f'Score = {percentage_score}%',  font=self.custom_font, bg=self.bg_color, fg=self.fg_color)
            if percentage_score > 79:
                self.score_label.config(fg=self.fg_color)
            elif percentage_score > 70:
                self.score_label.config(fg=self.fg_color)
            else:
                self.score_label.config(fg=self.fg_color)
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

    def destroy_radio_buttons(self):
        self.radiobutton1.grid_forget()
        self.radiobutton2.grid_forget()
        self.radiobutton3.grid_forget()
        self.radiobutton4.grid_forget()

    def create_radio_buttons(self):
        # Add radio buttons to the grid layout
        self.question.grid(row=0, column=0, columnspan=4, pady=5)
        self.radiobutton1.grid(row=1, column=1, sticky='W', pady=(0, 0))
        self.radiobutton2.grid(row=1, column=2, sticky='W', pady=(0, 0))
        self.radiobutton3.grid(row=2, column=1, sticky='W', pady=(0, 0))
        self.radiobutton4.grid(row=2, column=2, sticky='W', pady=(0, 0))
      
      
        self.radiobutton1.config(text=self.questions[self.current_index][1])
        self.radiobutton2.config(text=self.questions[self.current_index][2])
        self.radiobutton3.config(text=self.questions[self.current_index][3])
        self.radiobutton4.config(text=self.questions[self.current_index][4])

    def back_to_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_welcome_page()


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
            self.write_test_score()

    def write_test_score(self):
        # Open the CSV file in append mode
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile)
            
            # Write student ID and score to the CSV file
            csv_writer.writerow([self.student_id, self.score])

    def read_csv(self):
        try:
            file_path = os.path.abspath(self.filename)
            logging.info("Absolute path: %s", file_path)
            print("Absolute path:", file_path)
            with open(file_path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    self.questions.append(row)
                    self.num_of_test_questions += 1
        except Exception as e:
            error_message = f"Error loading the file: {str(e)}"
            print(error_message)
            logging.error(error_message)

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
        if not self.text:  
            print(f"Selected option: {selected_answer_value}")




    def nextquestion(self):
        self.checkanswer()
        self.question_number += 1
        self.current_index = (self.current_index + 1) % len(self.questions)
        self.question.config(text=self.questions[self.current_index][0])
        
        print("Updating radio button labels...")
        self.radiobutton1.config(text=self.questions[self.current_index][1])
        self.radiobutton2.config(text=self.questions[self.current_index][2])
        self.radiobutton3.config(text=self.questions[self.current_index][3])
        self.radiobutton4.config(text=self.questions[self.current_index][4])
        print(self.questions[self.current_index][1])
        print(self.questions[self.current_index][2])
        print(self.questions[self.current_index][3])
        print(self.questions[self.current_index][4])

        question_type = self.questions[self.current_index][-1]
        print(f"Question type: {question_type}")
        
        if question_type == "text":
            self.text = True
            self.destroy_radio_buttons()
            self.show_text_entry()
            self.selected_answer.set(None)  # Reset selected_answer variable to None for text questions
            # Move the Submit button to a different row
            self.next_button.grid(row=4, column=0, columnspan=4, pady=20)
        else:
            self.text = False
            self.hide_text_entry()
            self.enable_radio_buttons()
            self.create_radio_buttons()
            self.selected_answer.set(None)  # Reset selected_answer variable to None for text questions
            # Move the Submit button back to row 3
            self.next_button.grid(row=3, column=0, columnspan=4, pady=20)

      
        self.update_score_label()
        self.test_end()
        if self.test_over:
              self.next_button.config(text="Main Menu", command=self.back_to_main_menu)



if __name__ == '__main__':
    app = TestApp()
