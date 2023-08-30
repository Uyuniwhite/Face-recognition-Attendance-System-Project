import sys
import cv2
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from tensorflow.keras.models import load_model


class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.model = load_model("face_model.h5")
        self.cap = cv2.VideoCapture(0)
        self.class_names = self.list_directories('../img/face')

        self.initUI()

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

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel(self)
        layout.addWidget(self.label)

        self.start_btn = QPushButton('Start', self)
        self.start_btn.clicked.connect(self.start_webcam)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton('Stop', self)
        self.stop_btn.clicked.connect(self.stop_webcam)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)
        self.setWindowTitle('Face Recognition')
        self.show()

    def start_webcam(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret, image = self.cap.read()
        if ret:
            # Load haarcascade for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # Convert the color of the image to RGB from BGR for face detection
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Detect faces from the image
            faces = face_cascade.detectMultiScale(image_rgb, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            # If at least one face is detected, recognize it. Otherwise, display the whole frame.
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Crop the face and recognize it
                face_image = image[y:y + h, x:x + w]
                recognized_name = self.recognize_face(face_image)
                print('확인된 유저: ',recognized_name)

                # Display the name of the recognized person on the image
                image = cv2.putText(image, recognized_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                    cv2.LINE_AA)
            self.display_image(image)

    def stop_webcam(self):
        self.timer.stop()

    def recognize_face(self, image):
        prepared_img = self.prepare(image)
        predictions = self.model.predict(prepared_img)
        max_probability = np.max(predictions[0])
        print('확률', max_probability)
        return self.class_names[np.argmax(predictions[0])]

    # def recognize_face(self, image):
    #     ret, frame = self.cap.read()
    #     if not ret:
    #         return "Error reading frame"
    #
    #     face = self.prepare(frame)
    #     predictions = self.model.predict(face)
    #
    #     # 가장 확률이 높은 클래스의 확률을 얻습니다.
    #     max_probability = np.max(predictions[0])
    #     print('확률은', max_probability)
    #     # 임계값을 설정합니다. 이 값은 조절하셔서 원하는 결과를 얻을 때까지 실험하시면 됩니다.
    #     threshold = 0.7
    #
    #
    #     if max_probability > threshold:
    #         return self.class_names[np.argmax(predictions[0])]
    #     else:
    #         return "None"

    def prepare(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (80, 80))
        image = image.reshape(1, 80, 80, 1)
        image = image / 255.0
        return image

    def display_image(self, img):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        img = img.rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(img))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FaceRecognitionApp()
    sys.exit(app.exec_())
