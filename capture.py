import cv2
import mediapipe as mp
import math

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Simple gesture recognition function
def recognize_gesture(landmarks):
    """
    Example: detect three gestures (A, B, C) using distance ratios
    landmarks: list of 21 hand landmarks
    Returns: 'A', 'B', 'C' or 'Unknown'
    """
    # Example: measure distance from tip of thumb (4) to tip of index (8)
    x1, y1 = landmarks[4].x, landmarks[4].y
    x2, y2 = landmarks[8].x, landmarks[8].y
    distance = math.hypot(x2 - x1, y2 - y1)

    if distance < 0.05:
        return "A"
    elif distance < 0.1:
        return "B"
    elif distance < 0.15:
        return "C"
    elif distance < 0.20:
        return "D"
    elif distance < 0.25:
        return "E"
    elif distance < 0.3:
        return "F"
    elif distance < 0.35:
        return "G"
    elif distance < 0.4:
        return "H"
    elif distance < 0.45:
        return "I"
    elif distance < 0.49:
        return "J"
    elif distance < 0.51:
        return "K"
    elif distance < 0.55:
        return "L"
    elif distance < 0.6:
        return "M"
    elif distance < 0.64:
        return "N"
    elif distance < 0.68:
        return "O"
    elif distance < 0.72:
        return "P"
    elif distance < 0.75:
        return "Q"
    elif distance < 0.79:
        return "R"
    elif distance < 0.84:
        return "S"
    elif distance < 0.88:
        return "T"
    elif distance < 0.91:
        return "U"
    elif distance < 0.94:
        return "V"
    elif distance < 0.96:
        return "W"
    elif distance < 0.99:
        return "X"
    elif distance < 1:
        return "Y"
    else:
        return "Z"

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # mirror
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "None"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = recognize_gesture(hand_landmarks.landmark)

    cv2.putText(frame, f"Gesture: {gesture}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3)

    cv2.imshow("Sign Language Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
