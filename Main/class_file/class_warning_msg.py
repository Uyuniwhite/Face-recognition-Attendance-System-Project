from UI.warning_dialog import Ui_WarningDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import os
import sys


class MsgBox(QDialog, Ui_WarningDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 투명하게 함
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 클릭 이벤트
        self.ok_btn.clicked.connect(self.close)

    def set_dialog_type(self, type="", msg=""):
        import os

        # 작업 디렉토리를 현재 스크립트의 디렉토리로 변경
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        if type == 1:
            import os
            relative_path = "../../img/icon/check.png"

        if type == 2:
            relative_path = '../../img/icon/password.png'
            absolute_path = os.path.abspath(relative_path)
            msg = '얼굴인식이 어렵습니다. \n '\
                  '아이디와 비밀번호로 로그인 해 주세요!'

        absolute_path = os.path.abspath(relative_path)

        self.warn_lab.setText(msg)
        self.icon_lab.setScaledContents(True)
        self.icon_lab.setPixmap(QPixmap(absolute_path))
