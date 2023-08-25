from Main.UI.OpenWidget import Ui_OpenWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap

import sys

class OpenPage(QWidget, Ui_OpenWidget):
    def __init__(self, controller):
        super().__init__()

        self.setupUi(self)
        self.controller = controller
        self.setCursor(QCursor(QPixmap('../img/icon/cursor_1.png').scaled(40, 40)))

    def mousePressEvent(self, event):
        self.close()
        self.controller.login.show()