from Main.UI.UserCell import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap
import sys
import os



# 그리드 레이아웃에 들어가는 유저 캐럿셀
class UserCell(QWidget, Ui_Form):
    def __init__(self, parent, type, name):
        super().__init__()
        self.setupUi(self)
        self.main_page = parent

        # 상대경로 절대경로로 변환
        img_path = '../../img/icon/user.png'  # 유저 아이콘
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        absolute_path = os.path.abspath(img_path)

        # 이미지에 절대경로 담아주기
        self.img_lab.setScaledContents(True)
        self.img_lab.setPixmap(QPixmap(absolute_path))

        # 이름 담아주기
        self.name_lab.setText(name)

    def mousePressEvent(self, event):
        user_name = self.name_lab.text()
        self.main_page.summary_lab.setText(f'{user_name}의 {8}월 출근일수는 {00}일, 근태율은 {00}%입니다.')
        self.main_page.stackedWidget.setCurrentWidget(self.main_page.atd_page)
        # 여기서 유저의 이름 가지고 페이지 이동해야 함