from Main.UI.Opening import Ui_Opening
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
import os


class OpeningLoading(QWidget, Ui_Opening):
    Shown = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트의 위치
        path = os.path.join(current_dir, "..\..", "img", "icon", 'opening')
        self.label.setPixmap(QPixmap(path))
        self.Shown.connect(self.open_event)

    def open_event(self):
        pass