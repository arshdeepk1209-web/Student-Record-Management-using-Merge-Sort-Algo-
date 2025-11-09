import tkinter as tk
from tkinter import messagebox
import sqlite3
# Database Setup
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    marks INTEGER NOT NULL
)
""")
conn.commit()
# Merge Sort Implementation
def merge_sort_records(records):
    if len(records) > 1:
        mid = len(records) // 2
        left_half = records[:mid]
        right_half = records[mid:]
        merge_sort_records(left_half)
        merge_sort_records(right_half)
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] <= right_half[j][1]:
                records[k] = left_half[i]
                i += 1
            else:
                records[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            records[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            records[k] = right_half[j]
            j += 1
            k += 1
# GUI Application
class StableSortDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Stable Sorting")
        self.root.geometry("700x500")
        # Heading
        tk.Label(root, text="Student Record Management with Stable Merge Sort", font=("Arial", 14)).pack(pady=10)
        # Add Record Frame
        frame = tk.Frame(root)
        frame.pack(pady=5)
        tk.Label(frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Marks:", font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5) 
        self.marks_entry = tk.Entry(frame)
        self.marks_entry.grid(row=0, column=3, padx=5, pady=5)
        tk.Button(frame, text="Add Record", command=self.add_record, bg="green", fg="white", font=("Arial", 12)).grid(row=0, column=4, padx=5)
        # Buttons to view, sort, reset
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="View Records", command=self.view_records, bg="blue", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Sort Records by Marks", command=self.sort_records, bg="purple", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Reset All Records", command=self.reset_records, bg="red", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        # Output Text Box
        tk.Label(root, text="Records:", font=("Arial", 12)).pack(pady=5)
        self.output_text = tk.Text(root, height=20, width=80)
        self.output_text.pack(pady=5)
    # Add record to database
    def add_record(self):
        name = self.name_entry.get().strip()
        marks = self.marks_entry.get().strip()

        if not name or not marks:
            messagebox.showerror("Input Error", "Please enter both name and marks.")
            return

        try:
            marks = int(marks)
        except ValueError:
            messagebox.showerror("Input Error", "Marks must be an integer.")
            return

        cursor.execute("INSERT INTO students (name, marks) VALUES (?, ?)", (name, marks))
        conn.commit()
        messagebox.showinfo("Success", f"Record added: {name} - {marks}")
        self.name_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)

    # View records from database
    def view_records(self):
        cursor.execute("SELECT name, marks FROM students")
        records = cursor.fetchall()
        self.output_text.delete(1.0, tk.END)
        if records:
            for rec in records:
                self.output_text.insert(tk.END, f"{rec[0]}: {rec[1]}\n")
        else:
            self.output_text.insert(tk.END, "No records found.\n")

    # Sort records by marks using merge sort
    def sort_records(self):
        cursor.execute("SELECT name, marks FROM students")
        records = cursor.fetchall()
        if not records:
            messagebox.showinfo("Info", "No records to sort.")
            return

        records_list = list(records)
        merge_sort_records(records_list)  # sorted in-place

        self.output_text.delete(1.0, tk.END)
        for rec in records_list:
            self.output_text.insert(tk.END, f"{rec[0]}: {rec[1]}\n")

    # Reset all records from database
    def reset_records(self):
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to delete all records?")
        if confirm:
            cursor.execute("DELETE FROM students")
            conn.commit()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "All records have been deleted.\n")
            messagebox.showinfo("Reset Complete", "All records have been cleared.")

# ========================
# Run Application
# ========================
if __name__ == "__main__":
    root = tk.Tk()
    app = StableSortDBApp(root)
    root.mainloop()
