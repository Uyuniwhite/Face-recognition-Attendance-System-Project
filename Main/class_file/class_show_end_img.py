
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Main.class_file.class_font import Font


class CustomForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1120, 630)
        self.setStyleSheet("background-color: rgb(241, 242, 246);")

        self.verticalLayout = QVBoxLayout(self)
        self.verticalSpacer = QSpacerItem(20, 234, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(QPixmap('../../img/icon/end_logo.png'))
        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self)
        font1 = QFont()
        font1.setPointSize(20)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setText("이 화면은 자동으로 종료됩니다...5")
        self.label_2.setFont(Font.text(6))
        self.verticalLayout.addWidget(self.label_2)

        self.verticalSpacer_2 = QSpacerItem(20, 234, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomForm()
    window.show()
    sys.exit(app.exec_())
