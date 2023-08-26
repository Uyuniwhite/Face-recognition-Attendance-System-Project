from Main.UI.SaveUserImg import Ui_SaveUserImg
from PyQt5.QtWidgets import QWidget


# 외출 복귀 확인
class CheckOutWhile(QWidget, Ui_SaveUserImg):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller

        self.title_lab.setText('외출 확인 화면')


