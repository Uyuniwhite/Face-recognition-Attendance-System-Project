from Main.UI.SaveUserImg import Ui_SaveUserImg
from Main.class_file.class_face_detection import FaceRecognizer
from Main.class_file.class_warning_msg import MsgBox
from Main.class_file.class_font import Font
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal
import cv2
import os


# 외출 복귀 확인
class CheckOutWhile(QWidget, Ui_SaveUserImg):
    SetUserId = pyqtSignal(str)
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller

        self.title_lab.setText('외출 확인 화면')
        self.user_id = None

        self.msgbox = MsgBox()
        self.cancel_btn.clicked.connect(self.close)
        self.capture_btn.clicked.connect(self.start_cam)
        self.SetUserId.connect(self.set_user_id)

        self.user_img.setScaledContents(True)
        self.user_img.setPixmap(QPixmap("../../img/icon/face-id.png"))

        self.title_lab.setFont(Font.title(2))


    def set_user_id(self, user_id):
        self.user_id = user_id

    def var_for_cam(self):
        path = os.getcwd() + '\\face_model.h5'
        self.face_recognizer = FaceRecognizer(path)
        self.cap = cv2.VideoCapture(0)

    def start_cam(self):
        self.var_for_cam()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret, image = self.cap.read()

        if ret:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            faces = face_cascade.detectMultiScale(image_rgb, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            recognized_name = None
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                face_image = image[y:y + h, x:x + w]
                recognized_name = self.face_recognizer.recognize_face(face_image)

                label_color = (255, 0, 0)
                if recognized_name == "None":
                    label_color = (0, 0, 255)

                image = cv2.putText(image, recognized_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, label_color, 2,
                                    cv2.LINE_AA)
                result, name = self.face_recognizer.display_image(image, recognized_name, self.user_img)

                if result:
                    message = str()
                    if name == self.user_id:
                        message = f"{self.user_id}님 복귀하셨습니다."
                        self.msgbox.set_dialog_type(msg=message, img='check')
                    elif name != self.user_id:
                        message = f"당신은 {self.user_id}님이 아니신데요?"
                        self.msgbox.set_dialog_type(msg=message, img='warn')
                    self.msgbox.exec_()
                    self.cap.release()
                    break

            self.user_img.setPixmap(QPixmap("../../img/icon/face-id.png"))
            self.close()