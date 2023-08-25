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

        self.setupUi(self)
        self.initUI()
        self.set_font()

        # 컨트롤러 가져오기
        self.controller = controller

        # 그리드 레이아웃 생성
        self.gridLayout = QGridLayout(self.frame)
        self.set_grid_lay(team=None)  # 체크박스 변경될 때마다 set_grid_lay 호출되게 해야 함

    def initUI(self):

        # 커서 지정
        self.setCursor(QCursor(QPixmap('../img/icon/cursor_1.png').scaled(50, 50)))

        self.home_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.home_page)) # 관리자일 경우에는 팀 관리 화면으로 넘어가게 하기
        self.atd_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.atd_page))
        self.mypage_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.my_page))
        # self.home_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.home_page))

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
        self.dept_combobox.setFont(font_style_1)
        self.user_id_lineedit.setFont(font_style_1)
        self.pw_lineedit.setFont(font_style_1)
        self.pw_recheck_lineedit.setFont(font_style_1)







    def set_grid_lay(self, team):
        """그리드 영역에 위젯 클래스 넣어주기"""

        # 테스트 리스트(팀에 따라 다른 리스트 불러오는 부분 추가해야 함)
        test_list = [f'{n}번사원' for n in range(1, 21)]

        # 행의 개수를 원소 수에 따라 결정
        num_rows = (len(test_list) // 3)  # 올림 계산을 사용하여 행의 개수를 결정
        cnt = 0

        # 그리드 레이아웃에 유저셀 넣어주기
        for i in range(num_rows):
            for j in range(3):  # 열은 3개로 고정
                if cnt < len(test_list):  # test_list의 원소 수를 초과하지 않도록 함
                    user_cell = UserCell(self, type=1, name=test_list[cnt])
                    self.gridLayout.addWidget(user_cell, i, j)
                    cnt += 1
