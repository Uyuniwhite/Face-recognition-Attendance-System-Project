import sys
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from UI.LoginWidget import Ui_LoginWidget


class FaceDetection(QWidget, Ui_LoginWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = None

        # 웹캠 시작
        self.start_webcam()

        # 웹캠 중지 버튼 연결
        self.face_check_btn.clicked.connect(self.stop_webcam)

        # 얼굴 감지 활성화 플래그
        self.face_Enabled = True

        # 얼굴 감지를 위한 OpenCV의 Haar Cascade 로드
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def start_webcam(self):
        # 웹캠 초기화 및 해상도 설정
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        # 정기적으로 카메라 프레임을 가져오기 위한 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        # 웹캠에서 프레임 읽기
        ret, self.image = self.capture.read()

        # 이미지 미러링 (옵션)
        self.image = cv2.flip(self.image, 1)

        # 얼굴 감지가 활성화된 경우 감지 및 UI 업데이트, 그렇지 않으면 프레임만 표시
        if self.face_Enabled:
            detected_image = self.detect_face(self.image)
            self.displayImage(detected_image)
        else:
            self.displayImage(self.image)

    def detect_face(self, img):
        # 얼굴 감지를 위한 이미지를 회색조로 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 회색조 이미지에서 얼굴 감지
        faces = self.faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(90, 90))

        # 감지된 얼굴 주위에 사각형 그리기
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return img

    def stop_webcam(self):
        # 프레임 업데이트 중지를 위해 QTimer를 중지
        self.timer.stop()

    def displayImage(self, img):
        # OpenCV 이미지 형식을 PyQt의 QImage 형식으로 변환
        qformat = QImage.Format_RGB888 if len(img.shape) == 3 else QImage.Format_Indexed8
        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        # 이미지를 표시하기 위해 QLabel 위젯 업데이트
        self.sample_lab.setPixmap(QPixmap.fromImage(outImage))
        self.sample_lab.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FaceDetection()
    window.show()
    sys.exit(app.exec_())
