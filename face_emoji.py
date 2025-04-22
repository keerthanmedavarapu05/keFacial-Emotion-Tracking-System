
import cv2
import mediapipe as mp
import pyttsx3
import time
import random
import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd

# ✅ Init text-to-speech
speak_engine = pyttsx3.init()
speak_engine.setProperty('rate', 170)
voices = speak_engine.getProperty('voices')
# Try a different voice (pick the second one if available)
if len(voices) > 1:
    speak_engine.setProperty('voice', voices[1].id)
last_speak_time = 0

# ✅ MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# ✅ Webcam setup
cap = cv2.VideoCapture(0)

# ✅ Emoji list
all_emojis = [
    "😄", "😅", "😊", "😂", "😇", "🙃", "😉",
    "😌", "😍", "🥰", "😘", "🤩", "😎", "🤪",
    "😐", "😑", "🤨", "😔", "😞", "☹️", "😟",
    "😩", "😢", "😭", "😤", "😠", "😡", "😵", "😶‍🌫️"
]

# ✅ CSV logging setup
csv_file = "mood_log.csv"
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Mood Score", "Emoji", "Mood Text"])

# ✅ Custom mood logic
def calculate_mood_score_and_emoji(mouth_open, eye_open_level):
    if not mouth_open and eye_open_level < 0.015:
        mood_score = -10
        mood_text = "You look sad or tired."
    elif mouth_open and eye_open_level > 0.02:
        mood_score = 50
        mood_text = "You look shocked!"
    elif mouth_open:
        mood_score = 100
        mood_text = "You look happy!"
    elif eye_open_level > 0.02:
        mood_score = 75
        mood_text = "Neutral mood detected"
    else:
        mood_score = -10
        mood_text = "You look tired or sad."
    emoji = random.choice(all_emojis)
    return mood_score, emoji, mood_text

# ✅ Webcam loop
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            lm = face.landmark
            mouth_open = abs(lm[13].y - lm[14].y) > 0.05
            eye_open_level = abs(lm[159].y - lm[145].y)

            mood_score, emoji, mood_text = calculate_mood_score_and_emoji(mouth_open, eye_open_level)

            # Speak every 3s
            if time.time() - last_speak_time > 3:
                speak_engine.say(mood_text)
                speak_engine.runAndWait()
                last_speak_time = time.time()

            # Draw emoji + text
            cv2.putText(frame, emoji, (50, 120), cv2.FONT_HERSHEY_DUPLEX, 4.2, (0, 0, 0), 10)
            cv2.rectangle(frame, (50, 180), (50 + max(0, mood_score * 2), 220), (0, 255, 0), -1)
            cv2.putText(frame, f"Mood: {mood_score}", (50, 175), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)
            cv2.putText(frame, mood_text, (50, 260), cv2.FONT_HERSHEY_COMPLEX, 1.1, (0, 0, 0), 3)

            # Save to CSV
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mood_score, emoji, mood_text])

    cv2.imshow("🎯 Face Emoji + Mood Tracker", frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# 📊 Graph: average score per day
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date
    daily_avg = df.groupby('Date')['Mood Score'].mean()

    plt.figure(figsize=(10,6))
    daily_avg.plot(kind='bar', color='teal')
    plt.title("Average Mood Score Per Day")
    plt.ylabel("Average Score")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
