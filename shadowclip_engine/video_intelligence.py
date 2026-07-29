import cv2
import mediapipe as mp
import re


class VideoIntelligence:

    def __init__(self):

        # MediaPipe face detection
        self.mp_face = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.6
        )

    # -----------------------------------------------------

    def detect_face(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_face.process(rgb)

        if results.detections:
            return True

        return False

    # -----------------------------------------------------

    def analyze_video(self, video_path):

        cap = cv2.VideoCapture(video_path)

        frame_count = 0
        face_frames = 0

        while frame_count < 20:

            success, frame = cap.read()

            if not success:
                break

            if self.detect_face(frame):
                face_frames += 1

            frame_count += 1

        cap.release()

        if face_frames > 5:
            return "face"

        return "slides"

    # -----------------------------------------------------

    def optimize_hook(self, hook):

        if not hook:
            return "WATCH THIS"

        hook = hook.strip()

        # remove weird characters
        hook = re.sub(r'[^a-zA-Z0-9 ]+', '', hook)

        # limit number of words
        words = hook.split()

        if len(words) > 6:
            hook = " ".join(words[:6])

        # uppercase for thumbnails
        hook = hook.upper()

        # avoid empty result
        if len(hook) < 4:
            return "WATCH THIS"

        return hook