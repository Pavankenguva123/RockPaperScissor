import cv2
import mediapipe as mp
import numpy as np
import random
import pygame

# Initialize pygame for sound effects
pygame.init()
# win_sound = pygame.mixer.Sound("./assets/sounds/win.mp3")
# lose_sound = pygame.mixer.Sound("./assets/sounds/lose.mp3")
# uff_sound = pygame.mixer.Sound("./assets/sounds/uff.mp3")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Start webcam
cap = cv2.VideoCapture(0)

# Score tracking
scores = [0, 0]  # [AI, Player]

def get_finger_count(landmarks):
    """Detects number of extended fingers."""
    finger_tips = [8, 12, 16, 20]  # Tip points for index, middle, ring, pinky fingers
    count = 0
    for tip in finger_tips:
        if landmarks[tip][1] < landmarks[tip - 2][1]:  # Finger is up if tip is higher than lower joint
            count += 1
    return count

def determine_move(finger_count):
    """Maps finger count to a game move."""
    if finger_count == 0:
        return 1  # Rock
    elif finger_count >= 3:
        return 2  # Paper
    elif finger_count == 2:
        return 3  # Scissors
    return None

def play_game(player_move):
    """Compares moves and updates the game result."""
    global scores
    ai_move = random.randint(1, 3)

    if (player_move == 1 and ai_move == 3) or (player_move == 2 and ai_move == 1) or (player_move == 3 and ai_move == 2):
        scores[1] += 1
        # pygame.mixer.Sound.play(win_sound)
        return "Player Wins!"
    elif (player_move == 3 and ai_move == 1) or (player_move == 1 and ai_move == 2) or (player_move == 2 and ai_move == 3):
        scores[0] += 1
        # pygame.mixer.Sound.play(lose_sound)
        # pygame.mixer.Sound.play(uff_sound)
        return "AI Wins!"
    return "It's a Draw!"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip horizontally
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    player_move = None
    result_text = "Show Your Hand"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Convert landmarks to a list of coordinates
            landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
            finger_count = get_finger_count(landmarks)
            player_move = determine_move(finger_count)

            if player_move:
                result_text = play_game(player_move)

    # Display the game result
    cv2.putText(frame, f"AI: {scores[0]}  Player: {scores[1]}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, result_text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Rock Paper Scissors", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()