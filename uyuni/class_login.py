from UI.LoginWidget import Ui_LoginWidget
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import mediapipe as mp

class LoginFunc(QWidget, Ui_LoginWidget):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)

        self.main = controller

        self.mp_detection = mp.solutions.face_detection

        self.face_detection = self.mp_detection.FaceDetection(min_detection_confidence=0.5)

        self.video_capture = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret, frame_ = self.video_capture.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(frame)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                w += 70
                h += 70



        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)
        self.sample_lab.setPixmap(pixmap)

