import os
import sys

if __name__ == '__main__':
    os.system('pyuic5 LoginWidget.ui -o LoginWidget.py')
    os.system('pyuic5 MainWidget.ui -o MainWidget.py')
    os.system('pyuic5 warning_dialog.ui -o warning_dialog.py')
    os.system('pyuic5 OpenWidget.ui -o OpenWidget.py')
    os.system('pyrcc5 resource.qrc -o resource_rc.py')




# cd .\project\kiosk/ui
# python -m PyQt5.uic.pyuic -x main_ui.ui -o main_ui.py
