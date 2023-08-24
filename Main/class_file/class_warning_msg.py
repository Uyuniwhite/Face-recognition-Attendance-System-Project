from UI.warning_dialog import Ui_WarningDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
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
        img = None

        if type == 1:
            img = '../../img/icon/check.png'
        if type == 2:
            img = '../../img/icon/password.png'
            msg = '얼굴인식이 어렵습니다. \n '\
                  '아이디와 비밀번호로 로그인 해 주세요!'

        self.warn_lab.setText(msg)
        self.icon_lab.setPixmap(QPixmap(img))
