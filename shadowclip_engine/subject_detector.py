import cv2
import mediapipe as mp


class SubjectDetector:

    def __init__(self):

        # Face detector
        try:
            self.face = mp.solutions.face_detection.FaceDetection(
                model_selection=0,
                min_detection_confidence=0.6
            )
        except:
            self.face = None

        # Pose detector (body)
        try:
            self.pose = mp.solutions.pose.Pose()
        except:
            self.pose = None

    # -----------------------------------------------------

    def detect_face(self, frame):

        if not self.face:
            return False, None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face.process(rgb)

        if results.detections:

            det = results.detections[0]
            bbox = det.location_data.relative_bounding_box

            return True, bbox

        return False, None

    # -----------------------------------------------------

    def detect_body(self, frame):

        if not self.pose:
            return False

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if results.pose_landmarks:
            return True

        return False

    # -----------------------------------------------------

    def detect_subject(self, frame):

        # 1. face (mask included)
        has_face, bbox = self.detect_face(frame)

        if has_face:
            return "face", bbox

        # 2. body
        if self.detect_body(frame):
            return "body", None

        # 3. fallback = silhouette / AI
        return "unknown", None