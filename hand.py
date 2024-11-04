import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)

# Initialize MediaPipe Drawing
mp_drawing = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and find hands
    results = hands.process(rgb_frame)

    # Draw hand landmarks and box around the hand
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the wrist (landmark 0)
            h, w, _ = frame.shape
            wrist_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * w)
            wrist_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * h)

            # Draw a small red box around the wrist
            box_size = 20
            cv2.rectangle(frame, (wrist_x - box_size // 2, wrist_y - box_size // 2),
                          (wrist_x + box_size // 2, wrist_y + box_size // 2), (0, 0, 255), -1)

            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the resulting frame
    cv2.imshow('Hand Tracking', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
