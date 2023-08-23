from UI.LoginWidget import Ui_LoginWidget
from PyQt5.QtWidgets import QWidget

class LoginFunc(QWidget, Ui_LoginWidget):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)

        self.main = controller

