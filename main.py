import cv2
import numpy as np
import mediapipe as mp
from overlay import overlay_clothing, load_clothing

mp_pose = mp.solutions.pose

# Ruta al activo (ajusta a tu asset)
CLOTHING_PATH = 'assets/1.png'

def main():
    clothing_img, clothing_mask = load_clothing(CLOTHING_PATH)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                left_sh = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_sh = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left = (int(left_sh.x * frame.shape[1]), int(left_sh.y * frame.shape[0]))
                right = (int(right_sh.x * frame.shape[1]), int(right_sh.y * frame.shape[0]))
                mid = (int((left[0] + right[0]) / 2), int((left[1] + right[1]) / 2 + 0.07*frame.shape[0]))

                frame = overlay_clothing(frame, clothing_img, clothing_mask, left, right, mid)

            cv2.imshow('AR Mirror - Demo', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
