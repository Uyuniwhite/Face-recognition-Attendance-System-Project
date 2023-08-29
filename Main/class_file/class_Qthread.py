from Main.class_file.class_openingload import OpeningLoading
from PyQt5.QtCore import pyqtSignal, QThread

class Loading(QThread):
    finished_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.loading = OpeningLoading()
        self.loading.show()

    def run(self):
        self.finished_signal.emit()

    def loading_close(self):
        self.loading.close()



