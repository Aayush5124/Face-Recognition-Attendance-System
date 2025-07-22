# Face Recognition Attendance System

## Table of Contents
- [About The Project](#about-the-project)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## About The Project

This project implements an intelligent and automated **Attendance Management System** utilizing **Facial Recognition** technology. Developed using Python, it provides a user-friendly Tkinter-based graphical interface for seamless interaction. The system aims to streamline the attendance marking process in educational institutions or small businesses by replacing traditional methods with a fast, accurate, and touchless facial recognition approach.

The system allows for easy registration of new individuals (students/employees), trains a facial recognition model with their captured images, and then automatically marks attendance when recognized by the camera. All attendance records are stored for easy viewing and management.

## Features

* **User-Friendly GUI:** Intuitive interface built with Tkinter.
* **New Student/Employee Registration:**
    * Capture multiple facial images for a new individual.
    * Store enrollment number/ID and name.
* **Face Recognition Model Training:**
    * Trains an LBPH (Local Binary Patterns Histograms) Face Recognizer model using captured images.
    * Provides feedback on training status.
* **Automated Attendance Marking:**
    * Detects and recognizes faces in real-time using a webcam.
    * Automatically marks attendance for recognized individuals.
    * Records attendance with timestamp (date and time) in CSV format.
* **Attendance Viewing:**
    * Browse and view daily attendance records.
    * Option to view attendance for specific subjects/classes.
* **Error Handling & Notifications:**
    * Provides audio and visual feedback for various operations and errors.
    * Handles common issues like webcam access, invalid inputs, etc.
* **Robust Data Storage:**
    * Stores student/employee details in a CSV file (`StudentDetails/studentdetails.csv`).
    * Stores attendance records for each session/subject in separate CSV files.

## Technologies Used

* **Python 3.x:** The core programming language.
* **Tkinter:** For building the Graphical User Interface (GUI).
* **OpenCV (`cv2`):** For real-time facial detection, image capture, and face recognition.
* **NumPy:** For numerical operations, especially with image data.
* **Pillow (`PIL`):** For image processing capabilities, used with Tkinter.
* **Pandas:** For efficient data handling and manipulation of CSV files (e.g., attendance records).
* **`pyttsx3`:** For text-to-speech notifications and feedback.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Before you begin, ensure you have Python 3.x installed. You'll also need the following Python packages. You can install them using `pip`:

```bash
pip install opencv-python numpy pandas Pillow pyttsx3
Installation
Clone the repository:

Bash

git clone [https://github.com/Aayush5124/Face-Recognition-Attendance-System.git](https://github.com/Aayush5124/Face-Recognition-Attendance-System.git)
Navigate to the project directory:

Bash

cd Attendance-Management-system-using-face-recognition-master
Ensure necessary directories exist:
The application will create these automatically on first run or first save, but it's good to be aware:

TrainingImage/ (stores captured face images for training)

TrainingImageLabel/ (stores the trained model file Trainner.yml)

StudentDetails/ (stores studentdetails.csv)

Attendance/ (stores attendance records)

Place Haar Cascade File:
Ensure the haarcascade_frontalface_default.xml file is in the root of your project directory. This file is crucial for face detection.

Usage
Run the main application:

Bash
cd Attendance-Management-system-using-face-recognition-master
python attendance.py
This will open the main GUI window.

Register New Student:

Click "Register New Student".

Enter the student's Enrollment Number (numeric) and Name (alphabetic).

Click "Take Image". The webcam will activate and capture multiple images of the student's face. Look directly at the camera.

Once images are captured, the student's details will be saved.

Train Attendance Model:

After registering new students, click "Train Attendance Model".

This process trains the facial recognition algorithm using all captured images. A notification will confirm completion. This step is crucial for recognition to work.

Take Daily Attendance:

Click "Take Daily Attendance".

Select the subject for which attendance is to be marked.

The webcam will activate. As recognized faces appear, their attendance will be marked automatically.

Press 'q' to quit the webcam feed. Attendance is saved in a CSV file specific to the subject and date.

View Attendance Records:

Click "View Attendance Records".

Select the subject to view its attendance log. A new window will display the attendance data from the corresponding CSV file.

File Structure
Face-Recognition-Attendance-System/
├── attendance.py             # Main application GUI
├── takeImage.py              # Handles new student registration and image capture
├── trainImage.py             # Handles training the facial recognition model
├── automaticAttedance.py     # Handles automated attendance marking
├── show_attendance.py        # Handles viewing attendance records
├── haarcascade_frontalface_default.xml # Haar Cascade for face detection
├── UI_Image/                 # Folder for UI-related images (e.g., logo)
│   └── 0001.png              # Example logo image
├── TrainingImage/            # Stores captured face images (e.g., TrainingImage/123/face_image.jpg)
├── TrainingImageLabel/       # Stores the trained model (Trainner.yml)
├── StudentDetails/           # Stores student details (studentdetails.csv)
├── Attendance/               # Stores daily attendance records (e.g., Attendance/Math/Math_YYYY-MM-DD.csv)
└── README.md                 # This file
Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, feel free to:

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

License
Distributed under the MIT License. See LICENSE for more information (if you choose to add one).

Acknowledgements
OpenCV Documentation

Tkinter Documentation

pyttsx3 Documentation

Inspiration from various open-source face recognition projects.
