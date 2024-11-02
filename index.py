import sqlite3
import tkinter as tk
from tkinter import messagebox


class StudentDatabase:
    def __init__(self, db_name="students.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()
        self.seed_data()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    room_number TEXT NOT NULL
                )
            """)

    def seed_data(self):
        # Pre-existing data added to database only if no data exists
        students = [
            ("001", "Alice Smith", "A101"),
            ("002", "Bob Jones", "B202"),
            ("003", "Carol White", "C303")
        ]
        for student_id, name, room in students:
            self.add_student(name, student_id, room, save=False)

    def add_student(self, name, student_id, room_number, save=True):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO students (id, name, room_number) VALUES (?, ?, ?)",
                                  (student_id, name, room_number))
            if save:
                messagebox.showinfo("Success", "Student added successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists.")

    def delete_student(self, student_id):
        with self.conn:
            cursor = self.conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        if cursor.rowcount:
            messagebox.showinfo("Success", "Student deleted successfully.")
        else:
            messagebox.showerror("Error", "Student ID not found.")

    def search_student(self, student_id):
        cursor = self.conn.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        if row:
            return f"Name: {row[1]}, ID: {row[0]}, Room: {row[2]}"
        else:
            return "Student ID not found."

    def get_all_students(self):
        cursor = self.conn.execute("SELECT * FROM students")
        return cursor.fetchall()


class StudentApp:
    def __init__(self, root):
        self.database = StudentDatabase()
        self.root = root
        self.root.title("Student Management System")

        # Entry fields
        tk.Label(root, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(root, text="Student ID:").grid(row=1, column=0)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=1, column=1)

        tk.Label(root, text="Room Number:").grid(row=2, column=0)
        self.room_entry = tk.Entry(root)
        self.room_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add Student", command=self.add_student).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="Delete Student", command=self.delete_student).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Search Student", command=self.search_student).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="Display All Students", command=self.display_students).grid(row=6, column=0, columnspan=2)

        # Display area
        self.display_text = tk.Text(root, width=40, height=15)
        self.display_text.grid(row=7, column=0, columnspan=2)

        # Display all students initially
        self.display_students()

    def add_student(self):
        name = self.name_entry.get()
        student_id = self.id_entry.get()
        room_number = self.room_entry.get()
        self.database.add_student(name, student_id, room_number)
        self.clear_entries()
        self.display_students()

    def delete_student(self):
        student_id = self.id_entry.get()
        self.database.delete_student(student_id)
        self.clear_entries()
        self.display_students()

    def search_student(self):
        student_id = self.id_entry.get()
        student_info = self.database.search_student(student_id)
        self.display_text.delete("1.0", tk.END)
        self.display_text.insert(tk.END, student_info)

    def display_students(self):
        students = self.database.get_all_students()
        self.display_text.delete("1.0", tk.END)
        if students:
            for student in students:
                self.display_text.insert(tk.END, f"Name: {student[1]}, ID: {student[0]}, Room: {student[2]}\n")
        else:
            self.display_text.insert(tk.END, "No students in the database.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.room_entry.delete(0, tk.END)


# Run the application
root = tk.Tk()
app = StudentApp(root)
root.mainloop()
