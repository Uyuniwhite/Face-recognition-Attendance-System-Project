from Main.UI.AddEmployee import Ui_AddEmployee
from PyQt5.QtWidgets import QWidget

class AddEmpolyee(QWidget, Ui_AddEmployee):
    def __init__(self, controller):
        super().__init__()

        self.main = controller
        self.setupUi(self)


