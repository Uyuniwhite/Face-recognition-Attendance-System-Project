import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from Main.class_file.class_controller import Controller

def Main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = Controller()
    main_window.login.show()

    app.exec_()

if __name__ == '__main__':
    Main()
