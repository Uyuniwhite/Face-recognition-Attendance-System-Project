# 필요한 라이브러리와 모듈들을 임포트

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import sys
import cv2
import os
import numpy as np

from tensorflow.keras.models import load_model

class FaceRecognizer:
    def __init__(self, path):

        # h5_path = os.getcwd() + '\\class_file\\face_model.h5'
        h5_path = path
        self.model = load_model(h5_path)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "..\..", "img", "face")
        self.class_names = self.list_directories(path)

    def list_directories(self, path):
        """
        지정된 경로의 폴더를 출력합니다.
        """
        class_names = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path):
                class_names.append(name)
        return class_names

    def recognize_face(self, image):
        """얼굴 인식"""
        prepared_img = self.prepare(image)
        predictions = self.model.predict(prepared_img)
        max_probability = np.max(predictions[0])

        # 임계값 설정
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

    def display_image(self, img, name, display_lab):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        display_lab.setPixmap(QPixmap.fromImage(img))

        if name in self.class_names:
            print(f'{name}이 확인되었습니다.')
            return True, name
        else:
            return False, None