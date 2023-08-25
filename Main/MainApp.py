import sys

from PyQt5 import QtWidgets
from Main.class_file.class_controller import Controller
from PyQt5.QtGui import QFontDatabase

def Main():
    app = QtWidgets.QApplication(sys.argv)

    # 폰트 설정
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('../font/Pretendard-Black.ttf')
    fontDB.addApplicationFont('../font/Pretendard-Bold.ttf')
    fontDB.addApplicationFont('../font/Pretendard-ExtraBold.ttf')
    fontDB.addApplicationFont('../font/Pretendard-ExtraLight.ttf')
    fontDB.addApplicationFont('../font/Pretendard-Light.ttf')
    fontDB.addApplicationFont('../font/Pretendard-Medium.ttf')
    fontDB.addApplicationFont('../font/Pretendard-Regular.ttf')
    fontDB.addApplicationFont('../font/Pretendard-SemiBold.ttf')

    for family in fontDB.families():
        print(family, fontDB.styles(family))
    main_window = Controller()
    main_window.login.show()
    app.exec_()





if __name__ == '__main__':
    Main()
