import cv2
import numpy as np
import mediapipe as mp


class SmartFrameExtractor:

    def __init__(self):

        # Mediapipe face detector
        self.face_detector = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.6
        )

    def detect_face(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detector.process(rgb)

        if results.detections:
            return True

        return False

    def calculate_sharpness(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def extract_best_frame(self, video_path):

        cap = cv2.VideoCapture(video_path)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames == 0:
            raise RuntimeError("Video has no frames")

        sample_points = np.linspace(0, total_frames - 1, 30, dtype=int)

        best_frame = None
        best_score = -1

        for frame_number in sample_points:

            cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_number))
            success, frame = cap.read()

            if not success:
                continue

            sharpness = self.calculate_sharpness(frame)

            face_bonus = 0

            if self.detect_face(frame):
                face_bonus = 500

            score = sharpness + face_bonus

            if score > best_score:
                best_score = score
                best_frame = frame

        cap.release()

        if best_frame is None:
            raise RuntimeError("Could not extract good frame")

        return best_frame