import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TO-DO App")

        self.tasks = []
        self.load_tasks()

        # Task name
        tk.Label(root, text="Task Name").grid(row=0, column=0)
        self.task_name_entry = tk.Entry(root)
        self.task_name_entry.grid(row=0, column=1)

        # Task description
        tk.Label(root, text="Task Description").grid(row=1, column=0)
        self.task_desc_entry = tk.Entry(root)
        self.task_desc_entry.grid(row=1, column=1)

        # Date to complete the task
        tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=2, column=0)
        self.task_date_entry = tk.Entry(root)
        self.task_date_entry.grid(row=2, column=1)

        # Add task button
        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=3, column=0, columnspan=2)

        # Task list
        self.task_listbox = tk.Listbox(root, width=50, height=15)
        self.task_listbox.grid(row=4, column=0, columnspan=2)

        # Load tasks into the listbox
        self.refresh_task_listbox()

        # Mark as completed button
        self.complete_task_button = tk.Button(root, text="Mark as Completed", command=self.complete_task)
        self.complete_task_button.grid(row=5, column=0)

        # Delete task button
        self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.grid(row=5, column=1)

        # Sort tasks button
        self.sort_tasks_button = tk.Button(root, text="Sort by Date", command=self.sort_tasks_by_date)
        self.sort_tasks_button.grid(row=6, column=0, columnspan=2)

    def add_task(self):
        task_name = self.task_name_entry.get()
        task_desc = self.task_desc_entry.get()
        task_date = self.task_date_entry.get()

        # Validate date format
        try:
            datetime.strptime(task_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Invalid date format", "Please enter a valid date in YYYY-MM-DD format")
            return

        if task_name and task_desc and task_date:
            task = {"name": task_name, "desc": task_desc, "date": task_date, "completed": False}
            self.tasks.append(task)
            self.refresh_task_listbox()
            self.save_tasks()

            # Clear the entry fields
            self.task_name_entry.delete(0, tk.END)
            self.task_desc_entry.delete(0, tk.END)
            self.task_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing information", "Please fill out all fields")

    def refresh_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔" if task["completed"] else "✘"
            display_task = f"{task['name']} - {task['desc']} - {task['date']} [{status}]"
            self.task_listbox.insert(tk.END, display_task)

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index]["completed"] = True
            self.refresh_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Select a task", "Please select a task to mark as completed")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            self.refresh_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Select a task", "Please select a task to delete")

    def sort_tasks_by_date(self):
        self.tasks.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        self.refresh_task_listbox()
        self.save_tasks()

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task['name']}|{task['desc']}|{task['date']}|{task['completed']}\n")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                for line in file:
                    name, desc, date, completed = line.strip().split("|")
                    task = {"name": name, "desc": desc, "date": date, "completed": completed == "True"}
                    self.tasks.append(task)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
