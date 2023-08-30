import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Main.class_file.class_font import Font


class ShowEndImage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi()


    def setupUi(self):
        self.resize(1120, 630)
        self.setStyleSheet("background-color: rgb(241, 242, 246);")
        self.setWindowTitle('퇴근화면')
        self.setWindowFlags(Qt.FramelessWindowHint)

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
        self.label_2.setFont(Font.text(6, weight='light'))
        self.verticalLayout.addWidget(self.label_2)

        self.verticalSpacer_2 = QSpacerItem(20, 234, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_2)

    def start_timer(self):
        self.remaining_time = 5  # 초
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)  # 1초마다 timeout 시그널 발생

    def update_label(self):
        self.remaining_time -= 1
        self.label_2.setText(f"이 화면은 자동으로 종료됩니다...{self.remaining_time}")

        if self.remaining_time == 0:
            self.timer.stop()
            self.close()  # 5초 후 창 닫기


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = CustomForm()
#     window.show()
#     sys.exit(app.exec_())
