from UI.warning_dialog import Ui_WarningDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class MsgBox(QDialog, Ui_WarningDialog):
    def __init__(self, controller):
        super().__init__()

        self.setupUi(self)
        self.ok_btn.clicked.connect(self.close)

    def set_contents(self, msg, img):
        self.warn_lab.setText(msg)
        self.icon_lab.setPixmap(QPixmap(img))


