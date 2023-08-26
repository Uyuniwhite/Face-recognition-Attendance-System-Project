import cv2

from Main.UI.MainWidget import Ui_MainWidget
from Main.class_file.class_user_cell import UserCell
from Main.class_file.class_font import Font
from Main.class_file.class_face_detection import FaceRecognizer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtCore import pyqtSignal, QTimer
import sys
import os


class MainPage(QWidget, Ui_MainWidget):
    SetUserId = pyqtSignal(str)
    def __init__(self, controller):
        super().__init__()

        # 컨트롤러 가져오기
        self.controller = controller

        # 유저 Id
        self.user_id = None

        self.setupUi(self)
        self.initUI()  # 기본 설정
        self.initStyle() # 스타일 설정



    def initUI(self):
        self.home_btn.clicked.connect(
            lambda x: self.stackedWidget.setCurrentWidget(self.home_page))  # 관리자일 경우에는 팀 관리 화면으로 넘어가게 하기
        self.atd_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.atd_page))
        self.mypage_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.my_page))
        self.add_btn.clicked.connect(self.add_employee)  # 사원 추가
        self.team_search_btn.clicked.connect(self.set_grid_lay)
        self.out_btn.clicked.connect(self.show_out_while_img)

        # 부서 콤보박스에 넣기
        self.team_search_combobox.clear()
        depts = self.controller.dbconn.find_dept()
        self.team_search_combobox.addItems(depts)

        # 사원 등록 페이지 열기
        self.add_btn.clicked.connect(self.add_employee)

        # 테이블 채우기
        self.set_dept_table()

    def show_out_while_img(self):
        self.controller.show_out_img.show()


    def initStyle(self):
        # 커서 지정
        self.setCursor(QCursor(QPixmap('../img/icon/cursor_1.png').scaled(40, 40)))
        self.set_font()  # 폰트 설정

        # 퇴근하기 버튼 클릭
        self.end_btn.clicked.connect(self.clicked_end_btn)

        # 유저 아이디 설정 시그널 연결
        self.SetUserId.connect(self.set_user_id)

    # 사원 추가 버튼
    def add_employee(self):
        self.controller.add_emp.show()

    # 로그인 유저 ID 변수 설정
    def set_user_id(self, login_id):
        self.user_id = login_id

    # 폰트 설정
    def set_font(self):
        """폰트 지정"""
        font_style_1 = Font.text(1)

        # 상단버튼
        self.home_btn.setFont(Font.button(6))
        self.atd_btn.setFont(Font.button(6))
        self.mypage_btn.setFont(Font.button(6))
        self.users_btn.setFont(Font.button(6))

        # 마이페이지
        self.name_lab.setFont(font_style_1)
        self.dept_lab.setFont(font_style_1)
        self.user_id_lab.setFont(font_style_1)
        self.pw_lab.setFont(font_style_1)
        self.pw_recheck_lab.setFont(font_style_1)

        self.edit_btn.setFont(Font.button(6))

        self.name_lineedit.setFont(font_style_1)
        self.dept_lineedit.setFont(font_style_1)
        self.user_id_lineedit.setFont(font_style_1)
        self.pw_lineedit.setFont(font_style_1)
        self.pw_recheck_lineedit.setFont(font_style_1)

        # 근태화면
        self.attend_check_lab.setFont(Font.text(0, weight='bold'))
        self.attend_check_combobox.setFont(Font.text(0))
        self.attend_check_btn.setFont(Font.text(0, weight='bold'))
        self.summary_lab.setFont(Font.button(7))

        # 메인 페이지
        self.attend_day_lab.setFont(Font.title(3))
        self.out_day_lab.setFont(Font.title(3))
        self.absent_day_lab.setFont(Font.title(3))

        self.attend_text_lab.setFont(Font.text(1))
        self.out_text_lab.setFont(Font.text(1))
        self.absent_text_lab.setFont(Font.text(1))

        self.out_btn.setFont(Font.text(4))
        self.end_btn.setFont(Font.text(4))

        self.home_name_lab.setFont(Font.text(2))
        self.home_dept_lab.setFont(Font.text(2))
        self.graph_contents_1.setFont(Font.text(4))
        self.graph_contents_2.setFont(Font.text(4))
        self.graph_contents_3.setFont(Font.text(4))
        self.graph_contents_4.setFont(Font.text(4))

        # 관리자 페이지
        self.team_search_lab.setFont(Font.text(1, weight='bold'))
        self.team_search_btn.setFont(Font.text(1, weight='bold'))
        self.add_btn.setFont(Font.text(1, weight='bold'))
        self.team_search_combobox.setFont(Font.text(1))

    def set_grid_lay(self):
        """그리드 영역에 위젯 클래스 넣어주기"""
        self.clear_layout(self.users_grid_lay) #그리드 레이아웃 클리어

        current_dept = self.team_search_combobox.currentText()
        empolyee_list = self.controller.dbconn.select_dept(current_dept)

        # 행의 개수를 원소 수에 따라 결정
        num_rows = (len(empolyee_list) // 3 + 1)  # 올림 계산을 사용하여 행의 개수를 결정

        cnt = 0

        # 그리드 레이아웃에 유저셀 넣어주기
        for i in range(num_rows):
            for j in range(3):  # 열은 3개로 고정
                if cnt < len(empolyee_list):  # test_list의 원소 수를 초과하지 않도록 함
                    print(empolyee_list[cnt][0], empolyee_list[cnt][1])
                    user_cell = UserCell(self.controller, self, type=1, name=empolyee_list[cnt][0], user_id=empolyee_list[cnt][1])
                    self.users_grid_lay.addWidget(user_cell, i, j)
                    cnt += 1

    def clear_layout(self, layout: QLayout):
        """레이아웃 안의 모든 객체를 지웁니다."""
        if layout is None or not layout.count():
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
            # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
            else:
                self.clear_layout(item.layout())

    def set_dept_table(self):
        dept_list_test = self.controller.dbconn.info_dept()
        print(dept_list_test)
        self.dept_tablewidget.setRowCount(4) # 이건 부서 갯수 불러오기
        self.dept_tablewidget.setColumnCount(4)
        # self.dept_tablewidget.horizontalHeader().setVisible(False)  # 열 헤더를 숨깁니다.
        for idx, data in enumerate(dept_list_test):
            dept_code, dept_name, dept_emp = data
            self.dept_tablewidget.setItem(idx, 0, QTableWidgetItem(dept_name)) # 1번째 열, 1번째 행에 값 넣기
            self.dept_tablewidget.setItem(idx, 1, QTableWidgetItem(f'{dept_code}')) # 1번째 열, 2번째 행에 값 넣기
            self.dept_tablewidget.setItem(idx, 2, QTableWidgetItem(f"{dept_emp}")) # 1번째 열, 3번째 행에 값 넣기
            self.dept_tablewidget.setItem(idx, 3, QTableWidgetItem(f'{dept_name}근태율')) # 1번째 열, 4번째 행에 값 넣기
        self.dept_tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 열 너비를 조정합니다.

    # 퇴근하기 버튼 클릭 이벤트 코드
    def clicked_end_btn(self):
        print(os.getcwd())
        self.var_for_cam()
        self.start_cam()

    def var_for_cam(self):
        path = os.getcwd() + '\\face_model.h5'
        self.face_recognizer = FaceRecognizer(path)
        self.cap = cv2.VideoCapture(0)

    def start_cam(self):
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
                result, name = self.face_recognizer.display_image(image, recognized_name, self.face_lab)

                if result:
                    if name == self.user_id:
                        print("멀리안나갑니다")


