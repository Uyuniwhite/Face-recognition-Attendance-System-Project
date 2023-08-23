import sys
import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class FaceDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # MediaPipe 얼굴 인식 초기화
        self.mp_face = mp.solutions.face_detection
        self.face_detection = self.mp_face.FaceDetection(min_detection_confidence=0.2)
        self.mp_drawing = mp.solutions.drawing_utils

        # UI 초기화
        self.initUI()

    def initUI(self):
        # QLabel을 사용하여 화면에 카메라 이미지 출력
        self.image_label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 카메라 캡처 초기화
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("카메라를 열 수 없습니다.")
            sys.exit()

        # QTimer를 사용하여 일정 시간 간격으로 카메라 이미지를 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(20)  # 20ms마다 updateFrame 메서드 호출

        self.setWindowTitle('Face Detection App')
        self.resize(800, 600)
        self.show()

    def updateFrame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # 얼굴 인식 및 박스 그리기
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        if results.detections:
            for detection in results.detections:
                self.mp_drawing.draw_detection(frame, detection)

        # 카메라 이미지를 QLabel에 표시
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.cap.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FaceDetectionApp()
    sys.exit(app.exec_())
