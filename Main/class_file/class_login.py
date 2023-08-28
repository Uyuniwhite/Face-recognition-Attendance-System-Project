# 필요한 라이브러리와 모듈들을 임포트
from Main.UI.LoginWidget import Ui_LoginWidget
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QMessageBox, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QColor, QCursor
import sys
import cv2
import os
import numpy as np
from datetime import datetime
from Main.class_file.class_warning_msg import MsgBox
from Main.class_file.class_font import Font
from Main.class_file.class_face_detection import FaceRecognizer


# LoginFunc 클래스는 QWidget와 Ui_LoginWidget 클래스를 상속받아서 작성
class LoginFunc(QWidget, Ui_LoginWidget):
    def __init__(self, controller):
        super().__init__()  # 부모 클래스의 초기화 메서드를 호출

        # 초기변수
        self.user_name = None

        # 객체 생성
        self.main = controller
        self.msgbox = MsgBox()
        path = os.getcwd() + '\\class_file\\face_model.h5'
        self.face_recognizer = FaceRecognizer(path)

        self.setupUi(self)  # UI 설정을 초기화
        self.initUI()  # 초기 설정

        # 카메라로부터 영상을 캡처하기 위한 객체를 생성
        self.cap = cv2.VideoCapture(0)

    def initUI(self):
        # 그림자 효과를 설정
        self.set_shadow()

        # 웹캠 타이머 시작
        self.face_check_btn.clicked.connect(self.start_webcam)

        # 폰트 설정
        self.set_font()

        # 커서 설정
        self.setCursor(QCursor(QPixmap('../img/icon/cursor_1.png').scaled(40, 40)))

        # ID / PW 로그인 버튼 이벤트
        self.login_btn.clicked.connect(self.clicked_login_btn)

        # 사진 넣기
        self.face_lab.setScaledContents(True)
        self.face_lab.setPixmap(QPixmap('../img/icon/face-id.png'))

    def set_font(self):
        self.id_lab.setFont(Font.text(2, weight='light'))
        self.pw_lab.setFont(Font.text(2, weight='light'))
        self.login_btn.setFont(Font.text(2, weight='bold'))
        self.face_check_btn.setFont(Font.text(2, weight='bold'))
        self.id_lineedit.setFont(Font.text(2, weight='light'))
        self.pw_lineedit.setFont(Font.text(2, weight='light'))
        self.explain_lab.setFont(Font.text(2))

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
                recognized_name = self.face_recognizer.recognize_face(face_image)
                print(recognized_name)

                # 이미지에서 인식된 사람의 이름을 보여줌
                label_color = (255, 0, 0)  # 라벨 컬러 지정
                if recognized_name == "None":
                    label_color = (0, 0, 255)

                # 이미지 생성
                image = cv2.putText(image, recognized_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, label_color, 2,
                                    cv2.LINE_AA)
                result, name = self.face_recognizer.display_image(image, recognized_name, self.face_lab)

                # 인식된 이미지라면(유저라면)
                if result:
                    self.user_name = name
                    # 여기서 db 연결
                    check_result = self.save_db(login_type='face')

                    # 로그인시 캠 캡쳐 종료
                    self.cap.release()

                    # 사용자 타이틀 바 보여줌
                    self.show_title_btns()
                    self.main.leave_work.SetUserId.emit(self.user_name)
                    self.main.check_out.SetUserId.emit(self.user_name)

                    # 이 부분은 나중에 함수로 빼기
                    self.main.main_page.user_id = name
                    result = self.main.dbconn.get_user_data(name)
                    user_dept = self.main.dbconn.return_specific_data(column='dept_name', table_name='tb_dept', condition=f'dept_id = {result[4]}', type=1)
                    self.main.main_page.home_name_lab.setText(result[1])
                    self.main.main_page.home_dept_lab.setText(user_dept)

                    self.main.main_page.set_user_atd_combo(user_id=self.user_name)  # 유저 콤보박스 추가
                    self.main.main_page.set_user_atd_summary(user_id=self.user_name)  # 유저 근태내역 요약 추가

                    # 로그인 확인 다이얼로그 연결
                    message = f"{name}님 로그인되었습니다."
                    self.msgbox.set_dialog_type(msg=message, img='check')
                    self.msgbox.exec_()

                    # 메인 페이지 이동
                    self.main.leave_work.SetUserId.emit(self.user_name)
                    self.main.check_out.SetUserId.emit(self.user_name)
                    self.main.main_page.SetUserId.emit(self.user_name)
                    self.main.main_page.show()

                    # 타이머 종료
                    self.timer.stop()

                    # login 화면 종료
                    self.main.login.close()


                else:
                    self.msgbox.set_dialog_type(type=2)
                    self.msgbox.exec_()

    # ID / PW 입력하고 로그인버튼 클릭시 이벤트 처리 함수
    def clicked_login_btn(self):
        input_id, input_pw = self.id_lineedit.text(), self.pw_lineedit.text()

        result_id = self.verify_id(input_id)  # 아이디 검증
        result_pw = self.verify_pw(input_pw)  # 패스워드 검증
        message = ''
        if input_id != 'admin':
            if result_id == False or result_pw == False:
                self.msgbox.set_dialog_type(type=1)
            elif result_id == True and result_pw == True:
                db_password = self.main.dbconn.check_id_pw(input_id)  # 등록된 사원이면 패스워드가 담기고 등록되지않은 사원은 False가 담김
                if db_password == False:
                    self.msgbox.set_dialog_type(type=2)
                elif db_password != input_pw:
                    self.msgbox.set_dialog_type(type=3)
                else:
                    self.show_title_btns()
                    self.message = f"{input_id}님 로그인되었습니다."
                    self.msgbox.set_dialog_type(msg=message, img='check')

                    # 메인페이지로 이동
                    self.main.main_page.show()
                    # 로그인 정보 DB 저장
                    self.save_db('id')  # 사원 등록 True, False 반환, 로그인 타입 아이디
                    # login 화면 종료
                    self.main.login.close()

            self.msgbox.exec_()  # 메세지 박스 띄우기
        elif input_id == 'admin':
            # admin일 경우
            self.show_title_btns(type='admin')
            self.main.main_page.stackedWidget.setCurrentWidget(self.main.main_page.admin_dept_check)
            self.main.main_page.show()
            self.close()

    def show_title_btns(self, type='user'):
        btns_list = self.main.main_page.title_btns.findChildren(QPushButton)
        hidden_btns = []
        if type != 'admin':
            hidden_btns = ['users_btn']
        else:
            hidden_btns = ['users_btn', 'mypage_btn']

        for btn in btns_list:
            print(btn.objectName())
            btn.setVisible(btn.objectName() not in hidden_btns)

    # ID 검증
    def verify_id(self, input_id):
        if len(input_id) == 0 or ' ' in input_id:
            return False  # 아이디 길이가 0 이거나 아이디에 스페이스가 들어가있으면 False 리턴
        else:
            return True  # 이상없으면 true 리턴

    # PW 검증
    def verify_pw(self, input_pw):
        if len(input_pw) == 0 or ' ' in input_pw:
            return False  # 비밀번호 미입력 또는 스페이스 입력 시 False 리턴
        else:
            return True  # 이상없으면 true 리턴

    # 출근 시간 DB 저장
    def save_db(self, login_type):

        current_time = datetime.now()  # 현재 시간
        formatted_date = current_time.strftime('%Y-%m-%d')
        formatted_time = current_time.strftime('%H:%M:%S')
        day_date = formatted_date
        time_date = formatted_time
        check_result = self.main.dbconn.log_in(self.user_name, day_date, time_date, login_type)
        return check_result
