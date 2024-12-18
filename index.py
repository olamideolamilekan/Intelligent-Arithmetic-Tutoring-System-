from owlready2 import *
import tkinter as tk
from tkinter import messagebox, ttk
import random

import os
print(os.path.exists(r"C:\Users\SERIKI\Documents\ArtITS\Arithmetic_Tutoring_System.owl"))

# ontology
onto = get_ontology("C:/Users/SERIKI/Documents/ArtITS/Arithmetic_Tutoring_System.owl").load()

# Retrieve classes and properties from the ontology
ArithmeticOperation = onto.ArithmeticOperation
Addition = onto.Addition
Subtraction = onto.Subtraction
Multiplication = onto.Multiplication
Division = onto.Division
Operand = onto.Operand
Problem = onto.Problem
Feedback = onto.Feedback
operandValue = onto.operandValue
hasOperand = onto.hasOperand
hasSolution = onto.hasSolution
providesFeedback = onto.providesFeedback

# generating arithmetic problems based on their difficulties
def generate_problem(difficulty, operation_type):
    # Define number ranges based on difficulty
    if difficulty == 1:  # Easy: Single-digit numbers
        operand1_value = random.randint(1, 9)
        operand2_value = random.randint(1, 9)
    elif difficulty == 2:  # Medium: Two-digit numbers
        operand1_value = random.randint(10, 99)
        operand2_value = random.randint(10, 99)
    elif difficulty == 3:  # Hard: Three-digit numbers
        operand1_value = random.randint(100, 999)
        operand2_value = random.randint(100, 999)

   
    if operation_type == "Addition":
        result = operand1_value + operand2_value
    elif operation_type == "Subtraction":
        result = operand1_value - operand2_value
    elif operation_type == "Multiplication":
        result = operand1_value * operand2_value
    elif operation_type == "Division":
        if operand2_value == 0:
            result = None
        else:
            result = round(operand1_value / operand2_value, 2)

    return operand1_value, operand2_value, result


def create_problem(operation_type, operand1_value, operand2_value, result):
    problem = Problem(f"{operation_type}_Problem")
    feedback = Feedback(f"{operation_type}_Feedback")
    operand1 = Operand(f"{operation_type}_Operand1")
    operand2 = Operand(f"{operation_type}_Operand2")
    operand1.operandValue = operand1_value
    operand2.operandValue = operand2_value

    if operation_type == "Addition":
        operation = Addition(f"{operation_type}_Operation")
    elif operation_type == "Subtraction":
        operation = Subtraction(f"{operation_type}_Operation")
    elif operation_type == "Multiplication":
        operation = Multiplication(f"{operation_type}_Operation")
    elif operation_type == "Division":
        operation = Division(f"{operation_type}_Operation")
    
    operation.hasOperand = [operand1, operand2]
    problem.hasSolution = [operation]
    feedback.comment = [f"The result of the {operation_type.lower()} is {result}."]

    problem.providesFeedback = [feedback]
    return problem, feedback


class TutoringSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Intelligent Tutoring System")
        self.root.geometry("500x450")
        self.root.config(bg="#f0f4f8")  # Soft background color

        # Title
        title_label = tk.Label(root, text="Arithmetic Tutoring System", font=("Arial", 16, "bold"), bg="#f0f4f8", fg="#4a90e2")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Labels
        tk.Label(root, text="Select Operation:", font=("Arial", 12), bg="#f0f4f8", fg="#333333").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Label(root, text="Select Difficulty Level:", font=("Arial", 12), bg="#f0f4f8", fg="#333333").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        tk.Label(root, text="Operand 1:", font=("Arial", 12), bg="#f0f4f8", fg="#333333").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        tk.Label(root, text="Operand 2:", font=("Arial", 12), bg="#f0f4f8", fg="#333333").grid(row=4, column=0, padx=10, pady=10, sticky="e")

     
        self.operation_var = tk.StringVar()
        self.operation_var.set("Addition")
        self.operation_menu = ttk.Combobox(root, textvariable=self.operation_var, values=["Addition", "Subtraction", "Multiplication", "Division"], state="readonly", font=("Arial", 12))
        self.operation_menu.grid(row=1, column=1, padx=10, pady=10)

    
        self.difficulty_var = tk.IntVar()
        self.difficulty_var.set(1)
        self.difficulty_menu = ttk.Combobox(root, textvariable=self.difficulty_var, values=[1, 2, 3], state="readonly", font=("Arial", 12))
        self.difficulty_menu.grid(row=2, column=1, padx=10, pady=10)

       
        self.operand1_entry = tk.Entry(root, font=("Arial", 12), bg="#ffffff", fg="#333333", relief="solid", bd=2)
        self.operand2_entry = tk.Entry(root, font=("Arial", 12), bg="#ffffff", fg="#333333", relief="solid", bd=2)
        self.operand1_entry.grid(row=3, column=1, padx=10, pady=10)
        self.operand2_entry.grid(row=4, column=1, padx=10, pady=10)

    
        self.solve_button = tk.Button(root, text="Solve", command=self.solve_problem, font=("Arial", 12), bg="#4CAF50", fg="white", width=15, relief="raised")
        self.solve_button.grid(row=5, column=0, columnspan=2, pady=20)

       
        self.clear_button = tk.Button(root, text="Clear Fields", command=self.clear_fields, font=("Arial", 12), bg="#FF9800", fg="white", width=15, relief="raised")
        self.clear_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Feedback 
        self.feedback_label = tk.Label(root, text="Feedback:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#333333")
        self.feedback_label.grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.feedback_text = tk.Text(root, width=40, height=5, wrap="word", font=("Arial", 12), bg="#e8f5e9", fg="#2e7d32", relief="solid", bd=2)
        self.feedback_text.grid(row=7, column=1, padx=10, pady=10)

        
        self.help_button = tk.Button(root, text="Help", command=self.show_help, font=("Arial", 12), bg="#2196F3", fg="white", width=15, relief="raised")
        self.help_button.grid(row=8, column=0, columnspan=2, pady=10)

    def solve_problem(self):
        try:
            operation_type = self.operation_var.get()
            difficulty = self.difficulty_var.get()
            operand1_value, operand2_value, result = generate_problem(difficulty, operation_type)
            problem, feedback = create_problem(operation_type, operand1_value, operand2_value, result)

            # Display the result and feedback
            self.feedback_text.delete(1.0, tk.END)
            if result is None:
                self.feedback_text.insert(tk.END, f"Error: Division by zero is not allowed.")
            else:
                self.feedback_text.insert(tk.END, feedback.comment[0])

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_fields(self):
        self.operand1_entry.delete(0, tk.END)
        self.operand2_entry.delete(0, tk.END)
        self.feedback_text.delete(1.0, tk.END)

    def show_help(self):
        help_message = "This is an Arithmetic Intelligent Tutoring System.\n\n" \
                       "1. Select an operation (Addition, Subtraction, Multiplication, Division).\n" \
                       "2. Select difficulty level (1: Easy, 2: Medium, 3: Hard).\n" \
                       "3. Enter values for Operand 1 and Operand 2.\n" \
                       "4. Click 'Solve' to calculate the result.\n" \
                       "5. If there is any issue, please clear the fields and try again."
        messagebox.showinfo("Help", help_message)


if __name__ == "__main__":
    root = tk.Tk()
    app = TutoringSystemApp(root)
    root.mainloop()
