import tkinter as tk
from tkinter import *
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import time

# --- Color Palette (Consistent with main window) ---
PRIMARY_BG = "#212F3C"
SECONDARY_BG = "#2C3E50"
ACCENT_COLOR = "#D4AC0D"
TEXT_COLOR = "#FDFEFE"
ERROR_COLOR = "red"
SUCCESS_COLOR = "#2ECC71"

# This function is designed to be called from attendance.py
# Updated: added student_detail_path_arg to function signature
def TakeImageUI(parent_window, haarcasecade_path, trainimage_path, student_detail_path_arg, text_to_speech_func, err_screen_func):
    
    # Define message and txt1/txt2 in an outer scope accessible by TakeImage
    message = None # Will be defined later in the UI setup
    txt1 = None
    txt2 = None

    def TakeImage(Id, name):
        nonlocal message, txt1, txt2 # Declare these as non-local to access/modify them from the outer scope

        if not Id.isdigit() or not name.isalpha() or len(name) < 3: # Simple validation
            err_screen_func("Please enter valid Enrollment (numbers only) and Name (letters only, min 3 chars)!")
            text_to_speech_func("Invalid details entered. Please try again.")
            return

        cam = cv2.VideoCapture(0) # Open default camera
        if not cam.isOpened():
            err_screen_func("CRITICAL ERROR: Could not open webcam. Check if it's in use or privacy settings.")
            text_to_speech_func("Webcam could not be accessed. Please check your camera settings.")
            return

        harcascade = cv2.CascadeClassifier(haarcasecade_path)
        sampleNum = 0
        max_samples = 60 # Number of images to capture

        message.config(text=f"Capturing images for {name} (Enrollment: {Id}). Please look at the camera. {max_samples} images to go.",
                          fg=ACCENT_COLOR, bg=SECONDARY_BG)
        text_to_speech_func(f"Capturing images for {name}. Please look at the camera.")

        while True:
            ret, img = cam.read()
            if not ret or img is None:
                err_screen_func("Error reading frame from webcam during capture.")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = harcascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # Increment sample number and save the captured face
                sampleNum = sampleNum + 1
                
                # Create directory for student if it doesn't exist
                student_image_dir = os.path.join(trainimage_path, str(Id))
                if not os.path.exists(student_image_dir):
                    os.makedirs(student_image_dir)

                cv2.imwrite(os.path.join(student_image_dir, f"{name}.{Id}.{sampleNum}.jpg"), gray[y:y + h, x:x + w])
                
                message.config(text=f"Capturing images for {name} (Enrollment: {Id}). Please look at the camera. {max_samples - sampleNum} images to go.",
                                  fg=ACCENT_COLOR) # Update count

            cv2.imshow('Capturing Faces...', img)
            if sampleNum >= max_samples:
                break
            
            if cv2.waitKey(100) & 0xFF == ord('q'): # Press 'q' to quit early
                break

        cam.release()
        cv2.destroyAllWindows()

        if sampleNum >= max_samples:
            # Save student details to CSV
            res = "Images Saved for ID : " + Id + " Name : " + name
            row = [Id, name]
            try:
                # Ensure directory for student details exists
                student_details_dir = os.path.dirname(student_detail_path_arg) # Use the passed argument
                if not os.path.exists(student_details_dir):
                    os.makedirs(student_details_dir)

                with open(student_detail_path_arg, 'a+', newline='') as csvFile: # Use the passed argument
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
                message.config(text=res, bg=SUCCESS_COLOR, fg=TEXT_COLOR)
                text_to_speech_func(f"{name}'s images saved successfully! Now please train the model.")
            except Exception as e:
                err_screen_func(f"Error saving student details: {e}")
                message.config(text=f"Error saving details: {e}", bg=ERROR_COLOR, fg=TEXT_COLOR)
                text_to_speech_func("Error saving student details.")
        else:
            res = "Image capture cancelled or not enough samples."
            message.config(text=res, bg=ERROR_COLOR, fg=TEXT_COLOR)
            text_to_speech_func("Image capture was not completed.")

        # Clear input fields
        txt1.delete(0, END)
        txt2.delete(0, END)

    # --- UI for TakeImageUI Window ---
    ImageUI = tk.Toplevel(parent_window)
    ImageUI.title("Register Student Image")
    ImageUI.geometry("780x480")
    ImageUI.configure(background=PRIMARY_BG)
    ImageUI.resizable(0, 0)

    # Top Header Bar for TakeImageUI
    header_img_ui = tk.Frame(ImageUI, bg=SECONDARY_BG, relief=RIDGE, bd=10)
    header_img_ui.pack(fill=X)
    
    title_img_ui = tk.Label(
        header_img_ui, text="Register Your Face", bg=SECONDARY_BG, fg=TEXT_COLOR, font=("Verdana", 24, "bold"), pady=5
    )
    title_img_ui.pack()

    # Heading "Enter the details"
    details_heading = tk.Label(
        ImageUI,
        text="Enter Student Details",
        bg=PRIMARY_BG,
        fg=ACCENT_COLOR,
        font=("Verdana", 20, "bold"),
        pady=10
    )
    details_heading.place(x=250, y=80)

    # Enrollment No Label and Entry
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No:",
        width=15,
        height=2,
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        bd=5,
        relief=FLAT,
        font=("Verdana", 12),
    )
    lbl1.place(x=100, y=150)
    
    txt1 = tk.Entry(
        ImageUI,
        width=20,
        bd=5,
        validate="key",
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        relief=GROOVE,
        font=("Verdana", 16, "bold"),
        insertbackground=TEXT_COLOR
    )
    txt1.place(x=270, y=150)
    # Define testVal locally or pass it
    def local_testVal(inStr, acttyp):
        if acttyp == "1":
            if not inStr.isdigit():
                return False
        return True
    txt1["validatecommand"] = (txt1.register(local_testVal), "%P", "%d")

    # Name Label and Entry
    lbl2 = tk.Label(
        ImageUI,
        text="Student Name:",
        width=15,
        height=2,
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        bd=5,
        relief=FLAT,
        font=("Verdana", 12),
    )
    lbl2.place(x=100, y=220)
    
    txt2 = tk.Entry(
        ImageUI,
        width=20,
        bd=5,
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        relief=GROOVE,
        font=("Verdana", 16, "bold"),
        insertbackground=TEXT_COLOR
    )
    txt2.place(x=270, y=220)

    # Notification Label
    message = tk.Label( # Assign to the 'message' variable declared at the top of TakeImageUI
        ImageUI,
        text="Fill details and click 'Take Image'",
        width=50,
        height=2,
        bd=5,
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        relief=FLAT,
        font=("Verdana", 12, "italic"),
        wraplength=450
    )
    message.place(x=100, y=290)

    # Take Image Button
    take_img_btn = tk.Button(
        ImageUI,
        text="Take Image",
        command=lambda: TakeImage(txt1.get(), txt2.get()), # Calls the nested TakeImage function
        bd=8,
        font=("Verdana", 16, "bold"),
        bg=ACCENT_COLOR,
        fg=PRIMARY_BG,
        height=2,
        width=15,
        relief=GROOVE,
        activebackground="#A98A0A",
        activeforeground=TEXT_COLOR
    )
    take_img_btn.place(x=280, y=370)

    ImageUI.mainloop()