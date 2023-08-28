from Main.UI.ShowGraph import Ui_ShowGraph
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from Main.class_file.class_font import Font


class ShowGraph(QDialog, Ui_ShowGraph):
    def __init__(self, canvas):
        super().__init__()
        self.setupUi(self)

        self.verticalLayout.addWidget(canvas)
        self.pushButton.clicked.connect(self.close)