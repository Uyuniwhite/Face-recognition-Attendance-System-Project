import cv2

from Main.UI.MainWidget import Ui_MainWidget
from Main.class_file.class_user_cell import UserCell
from Main.class_file.class_font import Font
from Main.class_file.class_warning_msg import MsgBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize

import matplotlib.pyplot as plt
import cv2
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
        self.initStyle()  # 스타일 설정
        self.msgbox = MsgBox()  # 메세지박스 객체 싱성

    def initUI(self):
        # 페이지 이동
        # self.home_btn.clicked.connect(
        #     lambda x: self.stackedWidget.setCurrentWidget(self.home_page))  # 관리자일 경우에는 팀 관리 화면으로 넘어가게 하기
        self.home_btn.clicked.connect(self.move_homepage)
        self.atd_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.atd_page))  # 근태관리 페이지 이동
        self.mypage_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.my_page))  # 마이페이지 이동

        # 버튼 클릭 이벤트
        self.add_btn.clicked.connect(self.add_employee)  # 사원 추가 버튼 클릭시
        self.team_search_btn.clicked.connect(self.set_grid_lay)  # 팀 검색 버튼 눌렀을 때
        self.out_btn.clicked.connect(self.show_out_while_img)  # 외출하기 버튼 클릭
        self.end_btn.clicked.connect(self.clicked_end_btn)  # 퇴근하기 버튼 클릭
        self.attend_check_btn.clicked.connect(lambda x, y=self.user_id: self.show_atd_table(user_id=y))  # 특정 달 출근일자 테이블에 보여주기
        self.SetUserId.connect(self.set_user_id)
        self.mypage_btn.clicked.connect(self.get_userinfo_from_DB)  # 마이페이지 데이터 반영 관련
        self.edit_btn.clicked.connect(self.clicked_edit_btn)
        self.dept_tablewidget.cellDoubleClicked.connect(self.get_tbwid_data) # 테이블 위젯 셀 클릭 이벤트
        self.dept_tablewidget.setSelectionMode(QTableWidget.NoSelection) # 셀 클릭시 블록 설정 안되게
        self.emp_detail_check.clicked.connect(self.check_emp_info) # 관리자 사원 정보 확인 버튼 클릭
        self.back_to_dept_btn.clicked.connect(self.clicked_back_btn) # 관리자 사원관리 뒤로가기 버튼 이벤트

        # 부서 콤보박스에 넣기
        self.team_search_combobox.clear()
        depts = self.controller.dbconn.find_dept()
        self.team_search_combobox.addItems(depts)

        # 테이블 채우기
        self.set_dept_table()
        # 기본 클릭
        # self.team_search_btn.click()



    def show_atd_table(self, user_id):
        if user_id is not None:
            current_month = self.attend_check_combobox.currentText()
            atd_list = self.controller.dbconn.return_user_atd_info(user_id=user_id, year_month=current_month)

            self.tableWidget.setRowCount(len(atd_list))
            self.tableWidget.setColumnCount(6)

            for idx, data in enumerate(atd_list):
                date, start_time, end_time, atd_type = data[1], data[2], data[7], data[5]
                date_day = self.controller.dbconn.get_day_of_week(text_date=date)
                if end_time != 'NULL':
                    time_difference = self.controller.dbconn.get_strptime(start_time, end_time)
                else:
                    time_difference = '근무중'
                if atd_type == 'face':
                    atd_type = '얼굴인식'
                print(date, time_difference)

                # 각 아이템을 생성하고 가운데 정렬한 후, 테이블에 추가
                for col, value in enumerate([date, date_day, start_time, atd_type, end_time, time_difference]):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
                    self.tableWidget.setItem(idx, col, item)

            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def set_user_id(self, user_id):
        self.user_id = user_id

    # 유저 출근 달들만 리턴
    def set_user_atd_combo(self, user_id):
        user_atd_months = self.controller.dbconn.return_user_atd_month(user_id=user_id)
        self.attend_check_combobox.addItems(user_atd_months)
        self.attend_check_btn.click()

    # 근태화면 하단 요약 부분
    def set_user_atd_summary(self, user_id):
        text, user_atd_day, atd_per, absent_day = self.controller.dbconn.return_user_atd_summary(user_id=user_id)
        self.summary_lab.setText(text)
        self.atd_per_lab.setText(f"{str(atd_per)[:2]}%")
        self.attend_day_lab.setText(f'{str(user_atd_day)}일')
        self.out_day_lab.setText(f'{str(absent_day)}일')

    # 외출하기 버튼 클릭시
    def show_out_while_img(self):
        self.msgbox.set_dialog_type(type=5, img='question')
        self.msgbox.exec_()
        if self.msgbox.result() == 1:
            self.controller.show_out_img.show()

    # 퇴근하기 버튼 클릭시
    def clicked_end_btn(self):
        self.msgbox.set_dialog_type(type=6, img='question')
        self.msgbox.exec_()
        if self.msgbox.result() == 1:
            self.controller.leave_work.show()

    def initStyle(self):
        # 현재 우치ㅣ
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.setCursor(QCursor(QPixmap('../../img/icon/cursor_1.png').scaled(40, 40)))
        self.img_lab.setPixmap(QPixmap('../../img/icon/user.png').scaled(60, 60))

        self.back_to_dept_btn.setIcon(QIcon('../../img/icon/back.png'))
        self.back_to_dept_btn.setIconSize(QSize(40, 40))
        self.set_font()  # 폰트 설정

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
        self.emp_detail_check.setFont(Font.text(0, weight='bold'))
        self.summary_lab.setFont(Font.button(7))

        # 메인 페이지
        self.attend_day_lab.setFont(Font.title(3))
        self.out_day_lab.setFont(Font.title(3))
        self.atd_per_lab.setFont(Font.title(3))

        self.attend_text_lab.setFont(Font.text(1))
        self.out_text_lab.setFont(Font.text(1))
        self.atd_per_text_lab.setFont(Font.text(1))

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
        self.clear_layout(self.users_grid_lay)  # 그리드 레이아웃 클리어

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
                    user_cell = UserCell(self.controller, self, type=1, name=empolyee_list[cnt][0],
                                         user_id=empolyee_list[cnt][1])
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
        self.dept_tablewidget.setRowCount(len(dept_list_test))
        self.dept_tablewidget.setColumnCount(4)

        for idx, data in enumerate(dept_list_test):
            dept_code, dept_name, dept_emp = data
            dept_atd_per = self.controller.dbconn.return_team_atd_per(dept_name)

            # 각 항목 생성 및 중앙 정렬
            item_dept_name = QTableWidgetItem(dept_name)
            item_dept_name.setTextAlignment(Qt.AlignCenter)
            self.dept_tablewidget.setItem(idx, 0, item_dept_name)

            item_dept_code = QTableWidgetItem(f'{dept_code}')
            item_dept_code.setTextAlignment(Qt.AlignCenter)
            self.dept_tablewidget.setItem(idx, 1, item_dept_code)

            item_dept_emp = QTableWidgetItem(f"{dept_emp}")
            item_dept_emp.setTextAlignment(Qt.AlignCenter)
            self.dept_tablewidget.setItem(idx, 2, item_dept_emp)

            item_dept_rate = QTableWidgetItem(f'{str(dept_atd_per)}%')
            item_dept_rate.setTextAlignment(Qt.AlignCenter)
            self.dept_tablewidget.setItem(idx, 3, item_dept_rate)

        self.dept_tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # DB에서 데이터 user 데이터 가져와서 마이페이지에 데이터 반영
    def get_userinfo_from_DB(self):
        user_data = self.controller.dbconn.get_user_data(self.user_id)
        user_name = user_data[1]
        user_id = user_data[2]
        user_pw = user_data[3]
        dept_id = user_data[-1]
        dept_name = self.convert_dept_id_to_name(dept_id)
        self.set_userinfo_mypage(user_name, user_id, user_pw, dept_name)

    # 마이페이지 개인정보 넣기
    def set_userinfo_mypage(self, user_name, user_id, user_pw, dept_name):
        self.name_lineedit.setText(user_name)
        self.dept_lineedit.setText(dept_name)
        self.user_id_lineedit.setText(user_id)
        self.pw_lineedit.setText(user_pw)
        self.pw_recheck_lineedit.setText(user_pw)

    # 부서 번호를 부서 이름으로 변환
    def convert_dept_id_to_name(self, dept_id):
        dept_info = {10: "개발팀", 20: "인사팀", 30: "회계팀", 40: "감사팀", 50: "영업팀"}
        dept_name = dept_info[dept_id]
        return dept_name

    def clicked_edit_btn(self):
        self.controller.pw_change.user_id = self.user_id
        self.controller.pw_change.exec()

    # 관리자모드에서 부서관리 테이블위젯 데이터 가져오기
    def get_tbwid_data(self, row, col):
        dept_name = self.dept_tablewidget.item(row, 0).text()
        self.stackedWidget.setCurrentWidget(self.admin_home_page)
        idx = self.team_search_combobox.findText(dept_name)
        self.team_search_combobox.setCurrentIndex(idx)
        self.team_search_btn.click()

    # 홈버튼 이벤트
    def move_homepage(self):
        if self.user_id == 'admin':
            self.stackedWidget.setCurrentWidget(self.admin_dept_check)
            self.set_dept_table()
        else:
             self.stackedWidget.setCurrentWidget(self.home_page)

    def check_emp_info(self):
        self.controller.dept_change.show()

    def set_graph_for_user(self):
        """유저 그래프 넣기"""

        pass

    def clicked_back_btn(self):
        self.stackedWidget.setCurrentWidget(self.admin_home_page)