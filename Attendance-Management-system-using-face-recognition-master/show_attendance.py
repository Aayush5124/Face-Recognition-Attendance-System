import tkinter as tk
from tkinter import *
import pandas as pd
import csv
import os
import datetime
from tkinter import messagebox

# --- Color Palette (Consistent with main window) ---
PRIMARY_BG = "#212F3C"
SECONDARY_BG = "#2C3E50"
ACCENT_COLOR = "#D4AC0D"
TEXT_COLOR = "#FDFEFE"
ERROR_COLOR = "red"
SUCCESS_COLOR = "#2ECC71"

# Global path for attendance
attendance_base_path = "Attendance" # Ensure this matches attendance.py and automaticAttedance.py

def subjectchoose(text_to_speech_func):
    def calculate_attendance():
        sub = tx.get().strip()
        if not sub:
            messagebox.showwarning("Input Error", "Please enter the subject name!")
            text_to_speech_func("Please enter the subject name.")
            return

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        attendance_file = os.path.join(attendance_base_path, sub, f"{sub}_{current_date}.csv")

        if not os.path.exists(attendance_file):
            messagebox.showinfo("No Records", f"No attendance records found for '{sub}' on {current_date}.")
            text_to_speech_func(f"No attendance records found for {sub} today.")
            return

        try:
            df = pd.read_csv(attendance_file)
            
            # Display attendance in a new Tkinter window
            display_attendance_table(df, sub, current_date)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load attendance data: {e}")
            text_to_speech_func("Error loading attendance data.")

    def display_attendance_table(dataframe, subject_name, date_str):
        attendance_viewer = tk.Toplevel(subject)
        attendance_viewer.title(f"Attendance for {subject_name} on {date_str}")
        attendance_viewer.geometry("800x600") # Adjust size as needed
        attendance_viewer.configure(background=PRIMARY_BG)

        # Create a frame to hold the canvas and scrollbar
        container = tk.Frame(attendance_viewer, bg=PRIMARY_BG)
        container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg=PRIMARY_BG)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview, bg=SECONDARY_BG, troughcolor=PRIMARY_BG)
        scrollbar.pack(side=RIGHT, fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        inner_frame = tk.Frame(canvas, bg=PRIMARY_BG)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Display column headers
        for col_idx, col_name in enumerate(dataframe.columns):
            header_label = tk.Label(
                inner_frame,
                text=col_name,
                width=15,
                height=1,
                bg=SECONDARY_BG,
                fg=ACCENT_COLOR,
                font=("Verdana", 10, "bold"),
                relief=FLAT,
                padx=5, pady=2
            )
            header_label.grid(row=0, column=col_idx, sticky="nsew")

        # Display data rows
        for row_idx, row_data in dataframe.iterrows():
            for col_idx, cell_data in enumerate(row_data):
                # Custom color for '1' (Present) and '0' (Absent) for the date column
                if dataframe.columns[col_idx] == date_str:
                    bg_color = SUCCESS_COLOR if cell_data == 1 else ERROR_COLOR
                else:
                    bg_color = PRIMARY_BG # Default for other columns

                data_label = tk.Label(
                    inner_frame,
                    text=str(cell_data),
                    width=15,
                    height=1,
                    bg=bg_color,
                    fg=TEXT_COLOR,
                    font=("Verdana", 9),
                    relief=FLAT,
                    padx=5, pady=2
                )
                data_label.grid(row=row_idx + 1, column=col_idx, sticky="nsew")
        
        # Make columns expandable
        for col_idx in range(len(dataframe.columns)):
            inner_frame.grid_columnconfigure(col_idx, weight=1)

        # Update scroll region after all widgets are placed
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


    # --- GUI setup code for the subject selection window ---
    subject = tk.Toplevel()
    subject.title("View Attendance")
    subject.geometry("500x300")
    subject.resizable(0, 0)
    subject.configure(background=PRIMARY_BG)

    # Top Header Bar
    header_frame = tk.Frame(subject, bg=SECONDARY_BG, relief=RIDGE, bd=10)
    header_frame.pack(fill=X)
    
    title_label = tk.Label(
        header_frame,
        text="View Attendance Records",
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        font=("Verdana", 20, "bold"),
        pady=5
    )
    title_label.pack()

    # Label: "Enter Subject Name"
    sub_label = tk.Label(
        subject,
        text="Subject Name:",
        width=15,
        height=2,
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        bd=5,
        relief=FLAT,
        font=("Verdana", 12),
    )
    sub_label.place(x=50, y=100)

    # Entry Field for Subject Name
    tx = tk.Entry(
        subject,
        width=20,
        bd=5,
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        relief=GROOVE,
        font=("Verdana", 16, "bold"),
        insertbackground=TEXT_COLOR
    )
    tx.place(x=200, y=100)

    # Button to Calculate/Show Attendance
    show_btn = tk.Button(
        subject,
        text="Show Attendance",
        command=calculate_attendance,
        bd=7,
        font=("Verdana", 14, "bold"),
        bg=ACCENT_COLOR,
        fg=PRIMARY_BG,
        height=1,
        width=18,
        relief=GROOVE,
        activebackground="#A98A0A",
        activeforeground=TEXT_COLOR
    )
    show_btn.place(x=150, y=200)

    subject.mainloop()
    