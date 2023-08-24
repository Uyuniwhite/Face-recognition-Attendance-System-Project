import sys

from PyQt5 import QtWidgets
from class_controller import Controller

def Main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = Controller()
    main_window.login.show()
    # main_window.chatting.show()

    app.exec_()

if __name__ == '__main__':
    Main()
