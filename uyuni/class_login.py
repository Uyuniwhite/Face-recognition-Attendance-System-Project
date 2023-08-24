# 필요한 라이브러리와 모듈들을 임포트합니다.
from UI.LoginWidget import Ui_LoginWidget
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QColor
import cv2
import os
import mediapipe as mp
import numpy as np

# LoginFunc 클래스는 QWidget와 Ui_LoginWidget 클래스를 상속받아서 작성되었습니다.
class LoginFunc(QWidget, Ui_LoginWidget):
    def __init__(self, controller):
        super().__init__()  # 부모 클래스의 초기화 메서드를 호출
        self.setupUi(self)  # UI 설정을 초기화

        # controller를 이용해 메인 애플리케이션을 참조
        self.main = controller

        # 카메라로부터 영상을 캡처하기 위한 객체를 생성
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, 640)  # 너비 설정
        self.video_capture.set(4, 480)  # 높이 설정

        # 타이머 객체를 생성하고 update_frame 메서드를 연결, 5ms마다 이 메서드 호출
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

        # 그림자 효과를 설정
        self.set_shadow()

    # 그림자 효과를 위젯에 적용하는 메서드
    def set_shadow(self):
        self.making_shadow(self.left_widget)
        self.making_shadow(self.right_widget)

    def making_shadow(self, obj):
        shadow_effect_right = QGraphicsDropShadowEffect()
        shadow_effect_right.setOffset(10, 10)
        shadow_effect_right.setBlurRadius(20)
        shadow_effect_right.setColor(QColor(0, 0, 0, 80))
        obj.setGraphicsEffect(shadow_effect_right)

    # 카메라로부터 영상을 캡처하고 얼굴을 감지한 후 결과를 표시하는 메서드
    def update_frame(self):
        ret, frame = self.video_capture.read()  # 카메라로부터 한 프레임을 읽어옴
        if ret:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5, minSize=(30,30))

            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            self.sample_lab.setPixmap(pixmap)

    def closeEvent(self, event):
        self.video_capture.release()
        event.accept()


