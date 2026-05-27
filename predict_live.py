import cv2
import mediapipe as mp
import pickle
import numpy as np
import pyttsx3
import pandas as pd

# 🗣️ Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ✅ Load trained model
with open("sign_model.pkl", "rb") as f:
    model = pickle.load(f)

# 🖐️ Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# 🎥 Start webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_prediction = None

print("🟢 Starting live prediction. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 📍 Extract landmarks
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            # 🧠 Predict gesture
            if len(landmarks) == 63:
                df_input = pd.DataFrame([landmarks])
                current_prediction = model.predict(df_input)[0]

                # 🔁 Update only if gesture changes
                if current_prediction != last_prediction:
                    last_prediction = current_prediction
                    speak(f"The letter is {last_prediction}")

    # 🖼️ Display the last prediction
    if last_prediction:
        cv2.putText(frame, f"Prediction: {last_prediction}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Live Gesture Prediction", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("⏹️ Stopping live prediction.")
        break

cap.release()
cv2.destroyAllWindows()
