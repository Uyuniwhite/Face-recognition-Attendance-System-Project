import cv2

from Main.UI.MainWidget import Ui_MainWidget
from Main.class_file.class_user_cell import UserCell
from Main.class_file.class_font import Font
from Main.class_file.class_warning_msg import MsgBox
from Main.class_file.class_face_detection import FaceRecognizer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtCore import pyqtSignal, QTimer, QThread
import sys
import os





class MainPage(QWidget, Ui_MainWidget):

    def __init__(self, controller):
        super().__init__()

        # 컨트롤러 가져오기
        self.controller = controller

        # 유저 Id
        self.user_id = None

        self.setupUi(self)
        self.initUI()  # 기본 설정
        self.initStyle() # 스타일 설정
        self.msgbox = MsgBox()


    def initUI(self):
        self.home_btn.clicked.connect(
            lambda x: self.stackedWidget.setCurrentWidget(self.home_page))  # 관리자일 경우에는 팀 관리 화면으로 넘어가게 하기
        self.atd_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.atd_page))
        self.mypage_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.my_page))
        self.add_btn.clicked.connect(self.add_employee)  # 사원 추가 버튼 눌렀을 때
        self.team_search_btn.clicked.connect(self.set_grid_lay) # 팀 검색 버튼 눌렀을 때
        self.out_btn.clicked.connect(self.show_out_while_img) #

        # 부서 콤보박스에 넣기
        self.team_search_combobox.clear()
        depts = self.controller.dbconn.find_dept()
        self.team_search_combobox.addItems(depts)

        # 사원 등록 페이지 열기
        self.add_btn.clicked.connect(self.add_employee)

        # 테이블 채우기
        self.set_dept_table()


    # 근태 테이블 채우기
    def set_user_atd_info(self, user_id):
        pass

    # 근태화면 하단 요약 부분
    def set_user_atd_summary(self, user_id):
        # 유저 이름
        con = f"user_id = '{user_id}'" # 조건1
        user_name = self.controller.dbconn.return_specific_data(column='user_name', table_name='tb_user', condition=con)

        # 현재 년-월
        current_year_month = self.controller.dbconn.return_datetime(type='year_month')
        current_date = self.controller.dbconn.return_datetime(type='c_date')

        # 유저 번호
        user_no = self.controller.dbconn.find_no(user_id)

        # 출근일수
        con2 = f"user_no = {user_no} and atd_date like '%{current_year_month}%'" # 조건2
        user_atd_day = self.controller.dbconn.return_specific_data(column='count(*)', table_name='tb_atd', condition=con2, type=1)
        print(user_atd_day, current_date)
        # 근태율 계산 = (현재 달 출근일 / 현재 달 날짜) * 100
        atd_per = round((int(user_atd_day) / int(current_date)) * 100, 2)
        text = f'{user_name}님의 {current_year_month[-2:]}월 출근일수는 {user_atd_day}일, 근태율은 {atd_per}%입니다.'
        self.summary_lab.setText(text)

    def show_out_while_img(self):
        self.msgbox.set_dialog_type(type=5, img='question')
        self.msgbox.exec_()
        if self.msgbox.result() == 1:
            self.controller.show_out_img.show()


    def initStyle(self):
        # 커서 지정
        self.setCursor(QCursor(QPixmap('../img/icon/cursor_1.png').scaled(40, 40)))
        self.set_font()  # 폰트 설정

        # 퇴근하기 버튼 클릭
        self.end_btn.clicked.connect(self.clicked_end_btn)



    # 사원 추가 버튼
    def add_employee(self):
        self.controller.add_emp.show()

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
        self.controller.leave_work.show()





