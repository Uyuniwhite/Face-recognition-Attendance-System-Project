# 필요한 라이브러리와 모듈들을 임포트합니다.
from UI.LoginWidget import Ui_LoginWidget
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QColor
import cv2
import mediapipe as mp
import numpy as np
# from soyeon.image_learn import generator
from tensorflow.keras.models import load_model
import json

model = load_model('people.h5')
with open('class_indices.json', 'r') as f:
    class_indices = json.load(f)


# LoginFunc 클래스는 QWidget와 Ui_LoginWidget 클래스를 상속받아서 작성되었습니다.
class LoginFunc(QWidget, Ui_LoginWidget):
    def __init__(self, controller):
        super().__init__()  # 부모 클래스의 초기화 메서드를 호출
        self.setupUi(self)  # UI 설정을 초기화

        # controller를 이용해 메인 애플리케이션을 참조
        self.main = controller

        # mediapipe의 얼굴 감지 솔루션을 초기화
        self.mp_detection = mp.solutions.face_detection

        # 얼굴 감지 객체를 생성하고 최소 감지 신뢰도를 0.5로 설정
        self.face_detection = self.mp_detection.FaceDetection(min_detection_confidence=0.5)

        # 카메라로부터 영상을 캡처하기 위한 객체를 생성
        self.video_capture = cv2.VideoCapture(0)

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
        ret, frame_ = self.video_capture.read()  # 카메라로부터 한 프레임을 읽어옴
        if not ret:
            return

        # 프레임의 색상 공간을 BGR에서 RGB로 변환
        frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
        # 얼굴을 감지합니다.
        results = self.face_detection.process(frame)

        # 얼굴이 감지되면 그 위치에 사각형을 그린다
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                w += 70
                h += 70

                face_crop = frame[y:y + h, x:x + w]
                face_crop = cv2.resize(face_crop, (128, 128)) / 255.0  # 주의: 모델을 학습할 때 사용한 이미지 크기와 동일하게 조절
                # prediction = model.predict(np.expand_dims(face_crop, axis=0))

                # Predict
                predictions = model.predict(np.expand_dims(face_crop, axis=0))
                predicted_class = np.argmax(predictions, axis=1)
                predicted_label = list(class_indices.keys())[predicted_class[0]]

                if np.max(predictions) > 0.5:
                    # 인식된 얼굴에 대한 확률이 0.9보다 클 때 메세지박스 표시
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(f"{predicted_label} 얼굴이 감지되었습니다!")
                    msg.exec_()
                    # self.timer.stop()

        # QPixmap 객체를 생성하여 UI 레이블에 프레임을 표시
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)
        self.sample_lab.setPixmap(pixmap)
