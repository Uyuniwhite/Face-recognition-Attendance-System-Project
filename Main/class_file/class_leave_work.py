from Main.UI.SaveUserImg import Ui_SaveUserImg
from PyQt5.QtWidgets import QWidget


# 퇴근 확인
class CheckLeaveWork(QWidget, Ui_SaveUserImg):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller

        self.title_lab.setText('퇴근 확인 화면')
        self.numimglabel.setVisible(False)
        self.bottom_widget.setVisible(False)
