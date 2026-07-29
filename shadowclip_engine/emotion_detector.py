import cv2


class EmotionDetector:

    def __init__(self):

        # Haar cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # HOG person detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # -----------------------------------------------------

    def detect_person(self, frame):

        boxes, weights = self.hog.detectMultiScale(frame)

        return len(boxes) > 0

    # -----------------------------------------------------

    def detect_face(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        return len(faces) > 0

    # -----------------------------------------------------

    def detect_emotion(self, frame):

        # Simple heuristic emotion detection
        brightness = frame.mean()

        if brightness > 150:
            return "bright"

        if brightness < 70:
            return "dark"

        return "neutral"