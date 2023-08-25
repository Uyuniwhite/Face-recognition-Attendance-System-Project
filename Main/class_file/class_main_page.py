from Main.UI.MainWidget import Ui_MainWidget
from Main.UI.UserCell import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap
import sys
import os


# 그리드 레이아웃에 들어가는 유저 캐럿셀
class UserCell(QWidget, Ui_Form):
    def __init__(self, type ,name):
        super().__init__()
        self.setupUi(self)

        # 상대경로 절대경로로 변환
        img_path = '../../img/icon/user.png' # 유저 아이콘
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        absolute_path = os.path.abspath(img_path)

        # 이미지에 절대경로 담아주기
        self.img_lab.setScaledContents(True)
        self.img_lab.setPixmap(QPixmap(absolute_path))

        # 이름 담아주기
        self.name_lab.setText(name)


class MainPage(QWidget, Ui_MainWidget):
    def __init__(self, controller):
        super().__init__()

        self.setupUi(self)

        # 커서 지정
        self.setCursor(QCursor(QPixmap('../img/icon/cursor_1.png').scaled(50, 50)))



        # 그리드 레이아웃 생성
        self.gridLayout = QGridLayout(self.frame)
        self.set_grid_lay(team=None) # 체크박스 변경될 때마다 set_grid_lay 호출되게 해야 함



    def set_grid_lay(self, team):
        """그리드 영역에 위젯 클래스 넣어주기"""

        # 테스트 리스트(팀에 따라 다른 리스트 불러오는 부분 추가해야 함)
        test_list = [f'{n}번사원' for n in range(1,21)]


        # 행의 개수를 원소 수에 따라 결정
        num_rows = (len(test_list) // 3)  # 올림 계산을 사용하여 행의 개수를 결정
        cnt = 0

        # 그리드 레이아웃에 유저셀 넣어주기
        for i in range(num_rows):
            for j in range(3):  # 열은 3개로 고정
                if cnt < len(test_list):  # test_list의 원소 수를 초과하지 않도록 함
                    user_cell = UserCell(type=1, name=test_list[cnt])
                    self.gridLayout.addWidget(user_cell, i, j)
                    cnt += 1


        # 위젯 클릭하면 화면 전환
        # widgets = self.