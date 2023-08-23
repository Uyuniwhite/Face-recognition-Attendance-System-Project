from UI.login_page import Ui_LoginDialog
from PyQt5.QtWidgets import QWidget

class LoginFunc(QWidget, Ui_LoginDialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)

        self.main = controller

