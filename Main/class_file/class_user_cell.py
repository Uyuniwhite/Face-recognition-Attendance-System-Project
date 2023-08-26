from Main.UI.UserCell import Ui_Form
from Main.class_file.class_warning_msg import MsgBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap, QIcon

import sys
import os



# 그리드 레이아웃에 들어가는 유저 캐럿셀
class UserCell(QWidget, Ui_Form):
    def __init__(self, parent, type, name, user_id):
        super().__init__()
        self.setupUi(self)

        self.main_page = parent
        self.user_id = user_id
        self.user_name = name
        self.msgbox = MsgBox()

        # 커서 설정
        self.setCursor(QCursor(QPixmap('../../img/icon/cursor_1.png').scaled(40, 40)))

        # 상대경로 절대경로로 변환
        user_img_path = '../../img/icon/user.png'  # 유저 아이콘
        close_img_path = '../../img/icon/close_2.png'
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        user_img_absolute_path = os.path.abspath(user_img_path)
        close_img_absolute_path = os.path.abspath(close_img_path)

        # 이미지에 절대경로 담아주기
        self.img_lab.setScaledContents(True)
        self.img_lab.setPixmap(QPixmap(user_img_absolute_path))
        self.del_btn.setIcon(QIcon(close_img_absolute_path))

        # 이름 담아주기
        self.name_lab.setText(self.user_name)

        # 삭제 버튼 눌렀을 때 삭제하는 함수로 이동
        self.del_btn.clicked.connect(self.del_user)

        # 위젯 클릭하면 회원 확인 부분으로 이동하게 하기
        self.widget.mousePressEvent = self.move_main_page

    # 유저 삭제하는 부분
    def del_user(self):
        self.close() # 해당 위젯 삭제
        print(self.user_id, '삭제해야 합니다.')
        msg = f"{self.user_name}님을 삭제하시겠습니까?"
        self.msgbox.set_dialog_type(msg=msg, img='delete', type=4)
        self.msgbox.exec_()

        if self.msgbox.result() == 1:
            print('확인') # 여기서 db연결
        elif self.msgbox.result() == 0:
            print('취소')

    def move_main_page(self, event):
        user_name = self.name_lab.text()
        self.main_page.summary_lab.setText(f'{user_name}의 {8}월 출근일수는 {00}일, 근태율은 {00}%입니다.')
        self.main_page.stackedWidget.setCurrentWidget(self.main_page.atd_page)
