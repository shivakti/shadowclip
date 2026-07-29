import cv2
from subject_detector import SubjectDetector


class ViralFrameSelector:

    def __init__(self):

        self.detector = SubjectDetector()

    # -----------------------------------------------------

    def extract_best_frame(self, video_path):

        cap = cv2.VideoCapture(video_path)

        best_frame = None

        for i in range(30):  # analiza primeros frames

            success, frame = cap.read()

            if not success:
                break

            subject_type, bbox = self.detector.detect_subject(frame)

            # 🎯 prioridad: cara
            if subject_type == "face":
                cap.release()
                return frame

            # 🧠 guardar como posible
            if best_frame is None:
                best_frame = frame

        cap.release()

        return best_frame