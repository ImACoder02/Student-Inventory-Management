import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error

# Database class to handle all database interactions
class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',  # Change as needed
                user='root',       # Your database username
                password='',       # Your database password
                database='student_management'  # Database name
            )
            if self.connection.is_connected():
                print("Connected to MySQL Database")
        except Error as e:
            print(f"Error: {e}")
            raise

    def add_student(self, name, age, gender, course):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO students (name, age, gender, course) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, age, gender, course))
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
            raise

    def fetch_students(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM students"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            raise

    def update_student(self, student_id, name, age, gender, course):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE students SET name=%s, age=%s, gender=%s, course=%s WHERE id=%s"""
            cursor.execute(query, (name, age, gender, course, student_id))
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
            raise

    def delete_student(self, student_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM students WHERE id=%s"
            cursor.execute(query, (student_id,))
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
            raise

    def search_students(self, search_term, field):
        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM students WHERE {field} LIKE %s"
            cursor.execute(query, (f"%{search_term}%",))
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            raise

# Create a global instance of the Database class
db = Database()

# GUI-related functions
def add_student():
    if name_var.get() == "" or age_var.get() == "" or gender_var.get() == "" or course_var.get() == "":
        messagebox.showerror("Error", "All fields are required!")
        return
    try:
        db.add_student(name_var.get(), age_var.get(), gender_var.get(), course_var.get())
        fetch_students()
        clear_fields()
        messagebox.showinfo("Success", "Student added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding student: {e}")

def fetch_students():
    try:
        rows = db.fetch_students()
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching students: {e}")

def update_student():
    if selected_student is None:
        messagebox.showerror("Error", "Select a student to update!")
        return
    try:
        db.update_student(selected_student[0], name_var.get(), age_var.get(), gender_var.get(), course_var.get())
        fetch_students()
        clear_fields()
        messagebox.showinfo("Success", "Student updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error updating student: {e}")

def delete_student():
    if selected_student is None:
        messagebox.showerror("Error", "Select a student to delete!")
        return
    try:
        db.delete_student(selected_student[0])
        fetch_students()
        clear_fields()
        messagebox.showinfo("Success", "Student deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting student: {e}")

def select_student(event):
    global selected_student
    selected_student = student_table.item(student_table.focus())["values"]
    if selected_student:
        name_var.set(selected_student[1])
        age_var.set(selected_student[2])
        gender_var.set(selected_student[3])
        course_var.set(selected_student[4])

def clear_fields():
    name_var.set("")
    age_var.set("")
    gender_var.set("")
    course_var.set("")
    global selected_student
    selected_student = None

def search_student():
    search_term = search_var.get()
    search_field = search_by_var.get()
    if search_term == "":
        messagebox.showerror("Error", f"Please enter a {search_field} to search.")
        return
    try:
        results = db.search_students(search_term, search_field)
        student_table.delete(*student_table.get_children())
        if results:
            for row in results:
                student_table.insert("", "end", values=row)
        else:
            messagebox.showerror("Error", "No students found.")
    except Exception as e:
        messagebox.showerror("Error", f"Error searching students: {e}")

# GUI setup
root = tk.Tk()
root.title("Student Management System")
root.resizable(False, False)

# Variables
name_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
course_var = tk.StringVar()
search_var = tk.StringVar()
search_by_var = tk.StringVar(value="id")
selected_student = None

# Input fields
tk.Label(root, text="Name").grid(row=0, column=0)
tk.Entry(root, textvariable=name_var).grid(row=0, column=1)

tk.Label(root, text="Age").grid(row=1, column=0)
tk.Entry(root, textvariable=age_var).grid(row=1, column=1)

tk.Label(root, text="Gender").grid(row=2, column=0)
tk.Entry(root, textvariable=gender_var).grid(row=2, column=1)

tk.Label(root, text="Course").grid(row=3, column=0)
tk.Entry(root, textvariable=course_var).grid(row=3, column=1)

# Search feature
tk.Label(root, text="Search by").grid(row=0, column=2)
search_options = ["id", "name", "age", "gender", "course"]
search_menu = ttk.Combobox(root, textvariable=search_by_var, values=search_options, state="readonly")
search_menu.grid(row=0, column=3)
tk.Entry(root, textvariable=search_var).grid(row=0, column=4)
tk.Button(root, text="Search", command=search_student).grid(row=0, column=5)

# Buttons
tk.Button(root, text="Add", command=add_student).grid(row=4, column=0)
tk.Button(root, text="Update", command=update_student).grid(row=4, column=1)
tk.Button(root, text="Delete", command=delete_student).grid(row=4, column=2)
tk.Button(root, text="Clear", command=clear_fields).grid(row=4, column=3)
tk.Button(root, text="Show All", command=fetch_students).grid(row=4, column=4)

# Table
columns = ("ID", "Name", "Age", "Gender", "Course")
student_table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    student_table.heading(col, text=col)
student_table.grid(row=5, column=0, columnspan=6)
student_table.bind("<ButtonRelease-1>", select_student)

# Fetch initial data
fetch_students()

root.mainloop()
