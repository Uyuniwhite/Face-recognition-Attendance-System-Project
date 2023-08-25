from UI.MainWidget import Ui_MainWidget
from PyQt5.QtWidgets import *
import sys

class MainPage(QWidget, Ui_MainWidget):
    def __init__(self, controller):
        super().__init__()

        self.setupUi(self)
