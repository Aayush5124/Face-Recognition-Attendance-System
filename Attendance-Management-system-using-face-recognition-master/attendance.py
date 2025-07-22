import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module imports (ensure these files are in your project directory)
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Initialize pyttsx3 engine globally
engine = pyttsx3.init()
engine.setProperty('rate', 150) # You can adjust speaking rate

def text_to_speech(user_text):
    global engine
    engine.say(user_text)
    engine.runAndWait()

# --- Global Paths (Adjust if your project structure is different) ---
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)
studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# --- Color Palette ---
PRIMARY_BG = "#212F3C"
SECONDARY_BG = "#2C3E50"
ACCENT_COLOR = "#D4AC0D"
TEXT_COLOR = "#FDFEFE"
ERROR_COLOR = "red"
SUCCESS_COLOR = "#2ECC71"

# --- Main Window Setup ---
window = Tk()
window.title("CLASS VISION - Smart Attendance System") # Updated title
window.geometry("1280x720")
window.resizable(0, 0)
window.configure(background=PRIMARY_BG) # Primary Dark Blue/Teal

# --- Functions for pop-ups and actions ---
def del_sc1(): # For error screen
    sc1.destroy()

def err_screen(message_text="Enrollment & Name required!!!"): # Made message customizable
    global sc1
    sc1 = tk.Toplevel(window)
    sc1.geometry("400x150") # Slightly larger for better text fit
    sc1.title("Warning!")
    sc1.configure(background=SECONDARY_BG) # Secondary background for pop-up
    sc1.resizable(0, 0)
    
    tk.Label(
        sc1,
        text=message_text,
        fg=TEXT_COLOR, # Soft off-white text
        bg=SECONDARY_BG,
        font=("Verdana", 14, "bold"), # Smaller font for longer messages
        wraplength=380 # Wrap text within the label
    ).pack(pady=15, padx=10) # Added padding

    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg=TEXT_COLOR,
        bg=ACCENT_COLOR, # Accent Gold button
        width=10,
        height=1,
        activebackground="#A98A0A", # Darker gold on click
        font=("Verdana", 14, "bold"),
        relief=FLAT # Flat button style
    ).pack(pady=5)

# This function is used by Tkinter's validatecommand for Entry widgets
def testVal(inStr, acttyp):
    if acttyp == "1": # insert
        if not inStr.isdigit():
            return False
    return True

# This function creates and manages the Take Image UI (Registration Window)
def TakeImageUI():
    takeImage.TakeImageUI(
        window, # Pass the parent window for Toplevel
        haarcasecade_path,
        trainimage_path,
        studentdetail_path, # <--- IMPORTANT: Pass studentdetail_path here
        text_to_speech,
        err_screen # <--- IMPORTANT: Pass err_screen_func here
    )

# This function is a wrapper for the trainImage module function
def TrainImageUI(): # A UI wrapper for trainImage
    trainImage.TrainImage(
        haarcasecade_path,
        trainimage_path,
        trainimagelabel_path,
        main_notification_label, # Pass main window notification label
        text_to_speech,
        err_screen # Pass error screen function
    )

# This function is a wrapper for the automaticAttedance module function
def automatic_attedance_wrapper(): # Wrapper to call subjectChoose
    automaticAttedance.subjectChoose(text_to_speech)

# This function is a wrapper for the show_attendance module function
def view_attendance_wrapper(): # Wrapper to call subjectchoose from show_attendance
    show_attendance.subjectchoose(text_to_speech)

# Function to quit the application cleanly
def quit_application():
    window.destroy()

# --- UI Elements for Main Window ---

# Top Header Frame (combining logo and main title)
header_frame = tk.Frame(window, bg=SECONDARY_BG, relief=RIDGE, bd=10)
header_frame.pack(fill=X, pady=(0, 20)) # Added pady for spacing below header

# Logo (integrated into header)
try:
    logo_img = Image.open("UI_Image/0001.png")
    logo_img = logo_img.resize((80, 80), Image.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_frame, image=logo_tk, bg=SECONDARY_BG)
    logo_label.pack(side=LEFT, padx=20, pady=5)
except FileNotFoundError:
    print("Warning: UI_Image/0001.png not found. Skipping logo display.")
    logo_tk = None

# Main Title "CLASS VISION"
main_title = tk.Label(
    header_frame,
    text="CLASS VISION - SMART ATTENDANCE SYSTEM",
    bg=SECONDARY_BG,
    fg=TEXT_COLOR, # Soft off-white text
    font=("Verdana", 24, "bold"),
    padx=20,
    pady=10
)
main_title.pack(side=LEFT, expand=True, fill=X)


# Welcome Message below header
welcome_message = tk.Label(
    window,
    text="Welcome to Your Intelligent Attendance Solution!",
    bg=PRIMARY_BG, # Primary background
    fg=ACCENT_COLOR, # Accent gold for welcome message
    font=("Verdana", 28, "bold"),
    pady=20 # Spacing below welcome message
)
welcome_message.pack()


# Notification Label for general messages
main_notification_label = tk.Label(
    window,
    text="Please choose an option to begin.",
    bg=SECONDARY_BG, # Secondary background
    fg=TEXT_COLOR,
    width=60, # Wider to fit messages
    height=2,
    font=("Verdana", 14, "italic"),
    relief=FLAT,
    bd=5,
    wraplength=600 # Wrap text if message is long
)
main_notification_label.pack(pady=20)


# --- Buttons Layout (Centralized and grouped) ---
button_frame = tk.Frame(window, bg=PRIMARY_BG) # Frame for buttons
button_frame.pack(pady=10)

# Register Button
btn_register = tk.Button(
    button_frame,
    text="Register New Student",
    command=TakeImageUI,
    bd=7,
    font=("Verdana", 15, "bold"),
    bg=ACCENT_COLOR, # Accent gold
    fg=PRIMARY_BG, # Dark text for contrast on gold
    height=2,
    width=25,
    relief=GROOVE, # Groove for a slightly raised feel
    activebackground="#A98A0A", # Darker gold on click
    activeforeground=TEXT_COLOR # Light text on click
)
btn_register.grid(row=0, column=0, padx=20, pady=15) # Using grid for better layout control

# Train Model Button
btn_train = tk.Button(
    button_frame,
    text="Train Attendance Model",
    command=TrainImageUI,
    bd=7,
    font=("Verdana", 15, "bold"),
    bg=ACCENT_COLOR, # Accent gold
    fg=PRIMARY_BG,
    height=2,
    width=25,
    relief=GROOVE,
    activebackground="#A98A0A",
    activeforeground=TEXT_COLOR
)
btn_train.grid(row=0, column=1, padx=20, pady=15)

# Take Attendance Button
btn_take_attendance = tk.Button(
    button_frame,
    text="Take Daily Attendance",
    command=automatic_attedance_wrapper,
    bd=7,
    font=("Verdana", 15, "bold"),
    bg=ACCENT_COLOR, # Accent gold
    fg=PRIMARY_BG,
    height=2,
    width=25,
    relief=GROOVE,
    activebackground="#A98A0A", # CORRECTED: Changed from "#A980A" to "#A98A0A"
    activeforeground=TEXT_COLOR
)
btn_take_attendance.grid(row=1, column=0, padx=20, pady=15)

# View Attendance Button
btn_view_attendance = tk.Button(
    button_frame,
    text="View Attendance Records",
    command=view_attendance_wrapper,
    bd=7,
    font=("Verdana", 15, "bold"),
    bg=ACCENT_COLOR, # Accent gold
    fg=PRIMARY_BG,
    height=2,
    width=25,
    relief=GROOVE,
    activebackground="#A98A0A",
    activeforeground=TEXT_COLOR
)
btn_view_attendance.grid(row=1, column=1, padx=20, pady=15)

# Exit Button (positioned separately or at bottom center)
btn_exit = tk.Button(
    window,
    text="EXIT Application",
    command=quit_application,
    bd=7,
    font=("Verdana", 15, "bold"),
    bg=SECONDARY_BG, # Secondary color for exit, less prominent
    fg=TEXT_COLOR,
    height=2,
    width=20,
    relief=FLAT,
    activebackground=PRIMARY_BG, # Darker shade on click
    activeforeground=ACCENT_COLOR # Accent color on text when clicked
)
btn_exit.pack(pady=30) # Pushes it to the bottom

# --- Time and Date Label (placed at bottom right) ---
def update_time():
    time_string = time.strftime("%H:%M:%S")
    date_string = time.strftime("%d %b, %Y")
    time_date_label.config(text=f"{date_string}\n{time_string}")
    window.after(1000, update_time)

time_date_label = tk.Label(
    window,
    font=("Verdana", 12, "bold"),
    bg=PRIMARY_BG,
    fg=TEXT_COLOR,
)
time_date_label.place(relx=0.98, rely=0.98, anchor=SE) # Positioned at bottom right
update_time()


window.mainloop()
