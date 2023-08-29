from Main.UI.Opening import Ui_Opening
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal


class OpeningLoading(QWidget, Ui_Opening):
    Shown = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Shown.connect(self.open_event)

    def open_event(self):
        pass