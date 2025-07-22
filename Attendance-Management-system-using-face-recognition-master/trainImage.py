import cv2
import os
import numpy as np
from PIL import Image

# Placeholder for the main window's notification label, and text_to_speech function
# These will be passed from attendance.py or TakeImageUI
_global_notification_label = None
_global_text_to_speech_func = None
_global_err_screen_func = None

# --- Color Palette (Consistent with main window) ---
PRIMARY_BG = "#212F3C"
SECONDARY_BG = "#2C3E50"
ACCENT_COLOR = "#D4AC0D"
TEXT_COLOR = "#FDFEFE"
ERROR_COLOR = "red"
SUCCESS_COLOR = "#2ECC71"

# IMPORTANT: This function now correctly accepts 6 arguments
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, notification_label, text_to_speech_func, err_screen_func):
    global _global_notification_label, _global_text_to_speech_func, _global_err_screen_func
    _global_notification_label = notification_label
    _global_text_to_speech_func = text_to_speech_func
    _global_err_screen_func = err_screen_func

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = haarcasecade_path
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, IDs = getImagesAndLabels(trainimage_path, detector)
    
    if len(faces) == 0:
        msg = "No images found for training. Please register students first."
        _global_notification_label.config(text=msg, bg=ERROR_COLOR, fg=TEXT_COLOR)
        _global_text_to_speech_func(msg)
        return

    try:
        recognizer.train(faces, np.array(IDs))
        # Ensure directory for trainer.yml exists
        trainer_dir = os.path.dirname(trainimagelabel_path)
        if not os.path.exists(trainer_dir):
            os.makedirs(trainer_dir)
        recognizer.save(trainimagelabel_path)
        
        msg = "Model trained successfully!"
        _global_notification_label.config(text=msg, bg=SUCCESS_COLOR, fg=TEXT_COLOR)
        _global_text_to_speech_func(msg)
    except Exception as e:
        msg = f"Error during model training: {e}"
        _global_notification_label.config(text=msg, bg=ERROR_COLOR, fg=TEXT_COLOR)
        _global_text_to_speech_func(msg)
        _global_err_screen_func(msg)

def getImagesAndLabels(path, detector):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    faces = []
    IDs = []

    for student_dir in imagePaths:
        student_id = int(os.path.basename(student_dir)) # Assuming directory name is ID
        
        for image_file in os.listdir(student_dir):
            if image_file.endswith((".jpg", ".png", ".jpeg")):
                imagePath = os.path.join(student_dir, image_file)
                try:
                    pilImage = Image.open(imagePath).convert('L') # Convert to grayscale
                    img_numpy = np.array(pilImage, 'uint8')
                    
                    # Detect face from the image
                    face_rects = detector.detectMultiScale(img_numpy)
                    
                    for (x, y, w, h) in face_rects:
                        faces.append(img_numpy[y:y+h, x:x+w])
                        IDs.append(student_id)
                except Exception as e:
                    print(f"Error processing image {imagePath}: {e}")
                    # Optionally, you can update a UI message here too
    return faces, IDs
