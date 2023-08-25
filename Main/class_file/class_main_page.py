from Main.UI.MainWidget import Ui_MainWidget
from Main.class_file.class_user_cell import UserCell
from Main.class_file.class_font import Font
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap
import sys
import os


class MainPage(QWidget, Ui_MainWidget):
    def __init__(self, controller):
        super().__init__()

        # 컨트롤러 가져오기
        self.controller = controller

        self.setupUi(self)
        self.initUI()  # 기본 설정
        self.set_font()  # 폰트 설정

        # 그리드 레이아웃 생성
        self.main_v_lay = QVBoxLayout(self.scrollAreaWidgetContents)
        self.gridLayout = QGridLayout()

        self.main_v_lay.addLayout(self.gridLayout)
        self.grid_spacer = QSpacerItem(20, 231, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_v_lay.addItem(self.grid_spacer)

        # 현재 부서
        # 체크박스 변경될 때마다 set_grid_lay 호출되게 해야 함
        self.team_search_btn.clicked.connect(self.set_grid_lay)

    def initUI(self):

        # 커서 지정
        self.setCursor(QCursor(QPixmap('../img/icon/cursor_1.png').scaled(40, 40)))

        self.home_btn.clicked.connect(
            lambda x: self.stackedWidget.setCurrentWidget(self.home_page))  # 관리자일 경우에는 팀 관리 화면으로 넘어가게 하기
        self.atd_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.atd_page))
        self.mypage_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.my_page))
        self.add_btn.clicked.connect(self.add_employee)  # 사원 추가
        # self.home_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.home_page))

        # 부서 콤보박스에 넣기
        self.team_search_combobox.clear()
        depts = self.controller.dbconn.find_dept()
        self.team_search_combobox.addItems(depts)

    # 사원 추가 버튼
    def add_employee(self):

        pass

    # 폰트 설정
    def set_font(self):
        """폰트 지정"""
        font_style_1 = Font.text(1)

        # 상단버튼
        self.home_btn.setFont(Font.button(6))
        self.atd_btn.setFont(Font.button(6))
        self.mypage_btn.setFont(Font.button(6))

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

        # 관리자 페이지
        self.team_search_lab.setFont(Font.text(1, weight='bold'))
        self.team_search_btn.setFont(Font.text(1, weight='bold'))
        self.add_btn.setFont(Font.text(1, weight='bold'))
        self.team_search_combobox.setFont(Font.text(1))

    def set_grid_lay(self):
        """그리드 영역에 위젯 클래스 넣어주기"""

        current_dept = self.team_search_combobox.currentText()
        empolyee_list = self.controller.dbconn.select_dept(current_dept)
        print(empolyee_list)
        print(len(empolyee_list))

        for data in empolyee_list:
            name, user_id, dept = data[0], data[1], data[2]

        # 행의 개수를 원소 수에 따라 결정
        num_rows = (len(empolyee_list) // 3 + 1)  # 올림 계산을 사용하여 행의 개수를 결정

        cnt = 0

        # 그리드 레이아웃에 유저셀 넣어주기
        for i in range(num_rows):
            for j in range(3):  # 열은 3개로 고정
                if cnt < len(empolyee_list):  # test_list의 원소 수를 초과하지 않도록 함
                    print(empolyee_list[cnt][0], empolyee_list[cnt][1])
                    user_cell = UserCell(self, type=1, name=empolyee_list[cnt][0], user_id=empolyee_list[cnt][1])
                    self.gridLayout.addWidget(user_cell, i, j)
                    cnt += 1
