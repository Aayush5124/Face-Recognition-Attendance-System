import tkinter as tk
from tkinter import *
import cv2
import os
import time
import pandas as pd
import datetime
import csv
from tkinter import messagebox

# --- IMPORTANT: DEFINE YOUR FILE PATHS HERE (ensure consistency with attendance.py) ---
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"
# ------------------------------------------------------------------------------------

# --- Color Palette (Consistent with main window) ---
PRIMARY_BG = "#212F3C"
SECONDARY_BG = "#2C3E50"
ACCENT_COLOR = "#D4AC0D"
TEXT_COLOR = "#FDFEFE"
ERROR_COLOR = "red"
SUCCESS_COLOR = "#2ECC71"


# for choose subject and fill attendance
def subjectChoose(text_to_speech_func): # Renamed for clarity, it's a function passed
    def FillAttendance():
        sub = tx.get().strip() # Get subject name and remove leading/trailing whitespace
        if not sub: # Check if subject is empty after stripping
            t = "Please enter the subject name!"
            Notifica.configure(
                text=t,
                bg=ERROR_COLOR,
                fg=TEXT_COLOR,
                width=40, # Adjusted width
                font=("Verdana", 14, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech_func(t)
            return

        now = time.time()
        future = now + 20 # Webcam will run for 20 seconds
        print(f"Current time: {now}")
        print(f"Future time (20s later): {future}")

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(trainimagelabel_path)
        except Exception as e:
            error_msg = f"ERROR: Model not found. Please train the model. ({e})"
            Notifica.configure(
                text=error_msg,
                bg=ERROR_COLOR,
                fg=TEXT_COLOR,
                width=60,
                font=("Verdana", 12, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech_func(error_msg)
            print(error_msg)
            return

        facecasCade = cv2.CascadeClassifier(haarcasecade_path)
        if facecasCade.empty():
            error_msg = f"ERROR: Could not load Haar cascade classifier from {haarcasecade_path}. File might be missing or corrupted."
            Notifica.configure(
                text=error_msg,
                bg=ERROR_COLOR,
                fg=TEXT_COLOR,
                width=70,
                font=("Verdana", 10, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech_func(error_msg)
            print(error_msg)
            return

        try:
            df_students = pd.read_csv(studentdetail_path)
        except FileNotFoundError:
            error_msg = f"ERROR: Student details file not found at {studentdetail_path}."
            Notifica.configure(
                text=error_msg,
                bg=ERROR_COLOR,
                fg=TEXT_COLOR,
                width=70,
                font=("Verdana", 10, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech_func(error_msg)
            print(error_msg)
            return
        except Exception as e:
            error_msg = f"ERROR: Could not read student details file. Error: {e}"
            Notifica.configure(
                text=error_msg,
                bg=ERROR_COLOR,
                fg=TEXT_COLOR,
                width=70,
                font=("Verdana", 10, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech_func(error_msg)
            print(error_msg)
            return

        print("Attempting to open webcam...")
        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            error_msg = "CRITICAL ERROR: Could not open webcam. Check if it's in use, privacy settings, or drivers."
            Notifica.configure(
                text=error_msg,
                bg=ERROR_COLOR,
                fg=TEXT_COLOR,
                width=70,
                font=("Verdana", 10, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech_func(error_msg)
            print(error_msg)
            cv2.destroyAllWindows()
            return
        else:
            print("Webcam successfully opened.")

        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ["Enrollment", "Name"]
        attendance = pd.DataFrame(columns=col_names)
        
        while True:
            ret, im = cam.read()
            if not ret or im is None:
                print("Error: Could not read frame from webcam.")
                break
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = facecasCade.detectMultiScale(gray, 1.2, 5) # Scale factor and minNeighbors

            for (x, y, w, h) in faces:
                Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                if conf < 70: # Confidence threshold, lower is better match
                    
                    if Id in df_students["Enrollment"].values:
                        student_name = df_students.loc[df_students["Enrollment"] == Id]["Name"].values[0]
                    else:
                        student_name = "Unknown Student"
                    
                    label_text = f"{Id} - {student_name}"
                    
                    if Id not in attendance["Enrollment"].values:
                        attendance.loc[len(attendance)] = [Id, student_name]
                    
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 4) # Green rectangle for known
                    cv2.putText(im, label_text, (x, y - 10), font, 0.8, (0, 255, 0), 2) # Label above face
                else:
                    label_text = "Unknown"
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 4) # Red rectangle for unknown
                    cv2.putText(im, label_text, (x, y - 10), font, 0.8, (0, 0, 255), 2)

            if time.time() > future: # Stop after 20 seconds
                break

            cv2.imshow("Capturing Attendance...", im)
            key = cv2.waitKey(1) & 0xFF
            if key == 27: # Press 'Esc' to exit the camera window
                break

        cam.release()
        cv2.destroyAllWindows()

        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        
        # Ensure attendance directory exists
        subject_attendance_dir = os.path.join(attendance_path, sub)
        if not os.path.exists(subject_attendance_dir):
            os.makedirs(subject_attendance_dir)
        
        daily_attendance_file = os.path.join(subject_attendance_dir, f"{sub}_{date}.csv")
        
        if os.path.exists(daily_attendance_file):
            existing_df = pd.read_csv(daily_attendance_file)
            # Merge logic to update attendance for the day
            # Outer merge to include new students and existing ones
            updated_df = pd.merge(existing_df, attendance, on=['Enrollment', 'Name'], how='outer')
            
            # Fill existing attendance column for the current date.
            # Mark students present in the current session as '1'
            updated_df.loc[updated_df['Enrollment'].isin(attendance['Enrollment']), date] = 1
            # Mark students not present in the current session but present previously as '0' or NaN if you want to track absence
            updated_df[date] = updated_df[date].fillna(0).astype(int) # Fill missing values for the date with 0 and convert to int
            
            final_attendance_df = updated_df
        else:
            attendance[date] = 1 # Mark as 1 for present if new file
            final_attendance_df = attendance

        # Ensure 'Enrollment' and 'Name' are the first columns
        cols = ['Enrollment', 'Name'] + [col for col in final_attendance_df.columns if col not in ['Enrollment', 'Name']]
        final_attendance_df = final_attendance_df[cols]
        
        final_attendance_df.to_csv(daily_attendance_file, index=False)

        m = f"Attendance successfully filled for {sub}!"
        Notifica.configure(
            text=m,
            bg=SUCCESS_COLOR, # Green for success
            fg=TEXT_COLOR,
            width=40,
            relief=RIDGE,
            bd=5,
            font=("Verdana", 15, "bold"),
        )
        text_to_speech_func(m)
        Notifica.place(x=20, y=250)

        # Optional: Display CSV in a Tkinter table immediately after save
        display_attendance_csv(daily_attendance_file, sub)


    def display_attendance_csv(file_path, subject_name):
        csv_viewer_window = tk.Toplevel(subject) # Parent is subjectChoose window
        csv_viewer_window.title(f"Attendance Records for {subject_name}")
        csv_viewer_window.configure(background=PRIMARY_BG)
        
        frame = tk.Frame(csv_viewer_window, bg=PRIMARY_BG)
        frame.pack(fill=BOTH, expand=True)

        canvas = tk.Canvas(frame, bg=PRIMARY_BG)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        inner_frame = tk.Frame(canvas, bg=PRIMARY_BG)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        try:
            with open(file_path, newline="", encoding='utf-8') as file:
                reader = csv.reader(file)
                for r_idx, row_data in enumerate(reader):
                    for c_idx, cell_data in enumerate(row_data):
                        label = tk.Label(
                            inner_frame,
                            width=15, # Increased width for better data display
                            height=1,
                            fg=TEXT_COLOR if r_idx > 0 else ACCENT_COLOR, # Header in accent, data in text color
                            font=("Verdana", 10, "bold" if r_idx == 0 else "normal"), # Header bold
                            bg=SECONDARY_BG if r_idx == 0 else PRIMARY_BG, # Header with secondary bg, data with primary
                            text=cell_data,
                            relief=tk.FLAT, # Flat look
                            padx=5, pady=2
                        )
                        label.grid(row=r_idx, column=c_idx, sticky="nsew") # Use sticky for alignment
                
                # Make columns expandable
                for c_idx in range(len(row_data)):
                    inner_frame.grid_columnconfigure(c_idx, weight=1)

        except FileNotFoundError:
            messagebox.showerror("Error", f"Attendance file not found for {subject_name}. File was not created or there was an issue saving.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open attendance view: {e}")

    # --- Attf() function (Check Sheets) ---
    def Attf():
        sub = tx.get().strip()
        if not sub:
            t = "Please enter the subject name!"
            Notifica.configure(
                text=t,
                bg=ERROR_COLOR,
                fg=TEXT_COLOR,
                width=40,
                font=("Verdana", 14, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech_func(t)
            return
        
        current_date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
        # Construct the path to the daily attendance file for this subject and current date
        attendance_file_to_open = os.path.join(attendance_path, sub, f"{sub}_{current_date}.csv")
        
        # Check if file exists before trying to open it in an external program
        if os.path.exists(attendance_file_to_open):
            try:
                # Optionally, you can also call display_attendance_csv here to show it in Tkinter
                # instead of os.startfile. If you want to force external open, keep os.startfile.
                os.startfile(attendance_file_to_open)
                # display_attendance_csv(attendance_file_to_open, sub) # Uncomment to use internal viewer
            except Exception as e:
                error_msg = f"Error opening attendance sheet: {e}. Ensure you have a program to open .csv files."
                Notifica.configure(
                    text=error_msg,
                    bg=ERROR_COLOR,
                    fg=TEXT_COLOR,
                    width=70,
                    font=("Verdana", 10, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech_func(error_msg)
                print(error_msg)
        else:
            error_msg = f"Attendance sheet for '{sub}' on {current_date} not found. Please fill attendance first."
            Notifica.configure(
                text=error_msg,
                bg=ERROR_COLOR,
                fg=TEXT_COLOR,
                width=70,
                font=("Verdana", 10, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech_func(error_msg)
            print(error_msg)


    # --- GUI setup code for the subject window ---
    subject = tk.Toplevel() # Use Toplevel for pop-up window
    subject.title("Select Subject")
    subject.geometry("600x400") # Slightly larger for better spacing
    subject.resizable(0, 0)
    subject.configure(background=PRIMARY_BG)

    # Top Header Bar
    titl_frame = tk.Frame(subject, bg=SECONDARY_BG, relief=RIDGE, bd=10)
    titl_frame.pack(fill=X)
    
    titl_label = tk.Label(
        titl_frame,
        text="Enter Subject Details",
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        font=("Verdana", 24, "bold"),
        pady=5
    )
    titl_label.pack()

    # Label: "Enter Subject"
    sub_label = tk.Label(
        subject,
        text="Subject Name:",
        width=15, # Adjusted width
        height=2,
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        bd=5,
        relief=FLAT, # Flat style
        font=("Verdana", 14),
    )
    sub_label.place(x=80, y=100)

    # Entry Field for Subject Name
    tx = tk.Entry(
        subject,
        width=20, # Adjusted width
        bd=5,
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        relief=GROOVE, # Groove for input field
        font=("Verdana", 18, "bold"),
        insertbackground=TEXT_COLOR # Color of cursor
    )
    tx.place(x=250, y=100)

    # Notification Label (below input)
    Notifica = tk.Label(
        subject,
        text="Enter subject and click 'Fill Attendance'",
        bg=SECONDARY_BG,
        fg=TEXT_COLOR,
        width=50, # Wider to fit messages
        height=2,
        font=("Verdana", 12, "italic"),
        relief=FLAT,
        bd=5,
        wraplength=500 # Wrap text if message is long
    )
    Notifica.place(x=50, y=170)


    # --- Buttons ---
    btn_fill_attendance = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("Verdana", 15, "bold"),
        bg=ACCENT_COLOR, # Accent gold
        fg=PRIMARY_BG, # Dark text on gold
        height=2,
        width=15,
        relief=GROOVE,
        activebackground="#A98A0A",
        activeforeground=TEXT_COLOR
    )
    btn_fill_attendance.place(x=100, y=280)

    btn_check_sheets = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("Verdana", 15, "bold"),
        bg=SECONDARY_BG, # Secondary color, less prominent
        fg=TEXT_COLOR,
        height=2,
        width=15,
        relief=GROOVE,
        activebackground=PRIMARY_BG,
        activeforeground=ACCENT_COLOR
    )
    btn_check_sheets.place(x=350, y=280)

    subject.mainloop()