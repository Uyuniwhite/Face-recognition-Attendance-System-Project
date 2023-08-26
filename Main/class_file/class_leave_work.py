from Main.UI.SaveUserImg import Ui_SaveUserImg
from Main.class_file.class_face_detection import FaceRecognizer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, pyqtSignal
import cv2
import os


# 퇴근 확인
class CheckLeaveWork(QWidget, Ui_SaveUserImg):
    SetUserId = pyqtSignal(str)
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller

        self.title_lab.setText('퇴근 확인 화면')
        self.numimglabel.setVisible(False)
        self.init_cam()

    def init_cam(self):
        self.user_id = None
        # 유저 아이디 설정 시그널 연결
        self.SetUserId.connect(self.set_user_id)
        self.capture_btn.clicked.connect(self.start_cam)
        self.cancel_btn.clicked.connect(self.close)

    # 로그인 유저 ID 변수 설정
    def set_user_id(self, login_id):
        self.user_id = login_id

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
                print("퇴근 인식 카메라에 찍힌 당신의 이름은 ",recognized_name)

                label_color = (255, 0, 0)
                if recognized_name == "None":
                    label_color = (0, 0, 255)

                image = cv2.putText(image, recognized_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, label_color, 2,
                                    cv2.LINE_AA)
                result, name = self.face_recognizer.display_image(image, recognized_name, self.user_img)

                if result:
                    if name == self.user_id:
                        print("멀리안나갑니다")
                    elif name != self.user_id:
                        print(f"당신은 {self.user_id}님이 아니신데요?")

                    self.cap.release()
                    break
            self.close()
