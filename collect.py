import cv2
import mediapipe as mp
import pandas as pd
import os

# 🔤 Set the target letter for this session
target_letter = "no" \
  # Change this to "B", "C", ..., "Z" for each run

# 📁 Ensure the gesture_data folder exists
os.makedirs("gesture_data", exist_ok=True)

# 🖐️ Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# 🎥 Start webcam
cap = cv2.VideoCapture(0)
data = []

print(f"🟢 Collecting data for letter: {target_letter}")
print("Press 'q' to stop recording.")

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
            landmarks.append(target_letter)  # Add label
            data.append(landmarks)

    # 🖼️ Display frame
    cv2.putText(frame, f"Letter: {target_letter}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    cv2.imshow("Collecting Gesture Data", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 🛑 Cleanup
cap.release()
cv2.destroyAllWindows()

# 📊 Save data to CSV
columns = [f"{i}_{axis}" for i in range(21) for axis in ['x', 'y', 'z']] + ['label']
df = pd.DataFrame(data, columns=columns)
df.to_csv(f"gesture_data/{target_letter}_data.csv", index=False)

print(f"✅ Saved gesture data for '{target_letter}' to gesture_data/{target_letter}_data.csv")
