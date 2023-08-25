# 필요한 라이브러리와 모듈들을 임포트
from UI.LoginWidget import Ui_LoginWidget
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QColor
from datetime import datetime
import sys
import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model


# LoginFunc 클래스는 QWidget와 Ui_LoginWidget 클래스를 상속받아서 작성
class LoginFunc(QWidget, Ui_LoginWidget):
    def __init__(self, controller):
        super().__init__()  # 부모 클래스의 초기화 메서드를 호출

        # 초기변수
        self.class_names = None

        self.setupUi(self)  # UI 설정을 초기화
        self.initUI()  # 초기 설정

        # controller를 이용해 메인 애플리케이션을 참조
        self.main = controller

        # 학습한 모델 불러오기
        print(os.getcwd() + 'class\\face_model.h5')
        h5_path = os.getcwd() + '\\class_file\\face_model.h5'
        self.model = load_model(h5_path)

        # 카메라로부터 영상을 캡처하기 위한 객체를 생성
        self.cap = cv2.VideoCapture(0)

    def initUI(self):
        # 인식 가능한 이름 리스트
        self.class_names = ['soyeon', 'woohyun', 'hohyeon', 'gwanghyeon']

        # 그림자 효과를 설정
        self.set_shadow()

        # 웹캠 타이머 시작
        self.start_webcam()

    def start_webcam(self):
        """웹캠 시작하기"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    # 그림자 효과를 위젯에 적용하는 메서드
    def set_shadow(self):
        """위젯에 그림자 적용"""
        self.making_shadow(self.left_widget)
        self.making_shadow(self.right_widget)

    def making_shadow(self, obj):
        """객체 그림자 생성"""
        shadow_effect_right = QGraphicsDropShadowEffect()
        shadow_effect_right.setOffset(10, 10)
        shadow_effect_right.setBlurRadius(20)
        shadow_effect_right.setColor(QColor(0, 0, 0, 80))
        obj.setGraphicsEffect(shadow_effect_right)

    # 카메라로부터 영상을 캡처하고 얼굴을 감지한 후 결과를 표시하는 메서드
    def update_frame(self):
        ret, image = self.cap.read()
        if ret:
            # haarcascade 로드하여 얼굴 인식
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # 얼굴인식을 위해서 이미지 RGB 색 변환하기
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # 이미지에서 얼굴 인식
            faces = face_cascade.detectMultiScale(image_rgb, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            recognized_name = None
            # 최소 하나의 얼굴인 인식되면
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # 얼굴만 크롭한다
                face_image = image[y:y + h, x:x + w]
                recognized_name = self.recognize_face(face_image)
                print(recognized_name)

                # 이미지에서 인식된 사람의 이름을 보여줌
                label_color = (255, 0, 0)  # 라벨 컬러 지정
                if recognized_name == "None":
                    label_color = (0, 0, 255)

                # 이미지 생성
                image = cv2.putText(image, recognized_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, label_color, 2,
                                    cv2.LINE_AA)
            # 이미지 화면에 띄우기
            self.display_image(image, recognized_name)

    def recognize_face(self, image):
        """얼굴 인식"""
        prepared_img = self.prepare(image)
        predictions = self.model.predict(prepared_img)
        max_probability = np.max(predictions[0])
        print(max_probability)

        # 임계값을 설정합니다. 이 값은 조절하셔서 원하는 결과를 얻을 때까지 실험하시면 됩니다.
        threshold = 0.9
        if max_probability > threshold:
            return self.class_names[np.argmax(predictions[0])]
        else:
            return "None"

    def prepare(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (80, 80))
        image = image.reshape(1, 80, 80, 1)
        image = image / 255.0
        return image

    def display_image(self, img, name):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        self.sample_lab.setPixmap(QPixmap.fromImage(img))

        # if name in self.class_names:
        #     print(f'{name}이 확인되었습니다.')
        #     self.timer.stop()
        #     self.main.login.close()
        #     # self.main.msgbox.set_contents(img=None, msg='test').show()
        #     self.main.main_page.show()



