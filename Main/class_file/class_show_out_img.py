
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

class ShowOutForWhile(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.initUI()
        self.controller = controller

    def initUI(self):
        # 위젯의 크기 및 이름 설정
        self.setObjectName("MyWidget")
        self.resize(1120, 630)

        # 레이아웃 설정
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # 라벨 설정
        label = QLabel(self)
        label.setObjectName("label")
        label.setScaledContents(True)

        #이미지 적용
        current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트의 위치
        img_name = 'out_for_while.png'
        path = os.path.join(current_dir, "..\..", "img", "icon", img_name)

        label.setPixmap(QPixmap(path))

        # 라벨을 레이아웃에 추가
        layout.addWidget(label)

        # 외출 복귀 화면 클릭하면
        label.mousePressEvent = self.check_user

    # 사용자 확인
    def check_user(self, event):
        print('사용자 외출 복귀 화면으로 이동해야 함')
        self.close()
        self.controller.check_out.show()
        pass
        # 사용자 확인 페이지로 이동

