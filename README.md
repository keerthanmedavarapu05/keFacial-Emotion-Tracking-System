# AI Mood Tracker

A real-time AI-based mood tracking system that uses your webcam to detect facial expressions and classify your emotional state.

## Features

- Real-time face tracking using **MediaPipe**
- Emoji-based emotion detection (happy, tired, shocked, neutral)
- Dynamic voice feedback using **pyttsx3**
- Smart logic to detect tired/sad state (mouth closed + droopy eyes)
- Logs mood scores to CSV
- Graphs average daily mood score with **Matplotlib**

## Tech Stack

- Python
- OpenCV
- MediaPipe
- pyttsx3
- Matplotlib
- Pandas

## How It Works

1. Launch the script (`python face_emoji_mood_tracker_daily_score.py`)
2. Make expressions — happy, shocked, tired
3. Script reacts with an emoji, voice comment, and logs the score
4. After you press **Esc**, a graph appears showing your **daily mood summary**

## Installation

```bash
pip install opencv-python mediapipe pyttsx3 matplotlib pandas
```

## Files

- `face_emoji_mood_tracker_daily_score.py` – main script
- `mood_log.csv` – auto-created log file
- `requirements.txt` – all libraries used
- `README.md` – this file

## Credits

Built by Sai Keerthan  
For AI/dev roles – open to opportunities!

## Let’s Connect

- LinkedIn: https://www.linkedin.com/in/sai-keerthan-0a4a50313/

