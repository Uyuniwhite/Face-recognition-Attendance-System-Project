from Main.UI.Opening import Ui_Opening
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread, pyqtSignal


class OpeningLoading(QWidget, Ui_Opening):
    Shown = pyqtSignal()

    def __init__(self, controller=None):
        super().__init__()
        self.setupUi(self)

        self.controller = controller
        self.Shown.connect(self.open_event)

    def open_event(self):
        self.close()
