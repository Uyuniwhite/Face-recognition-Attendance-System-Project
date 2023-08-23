import os
import sys

if __name__ == '__main__':
    os.system('pyuic5 login_page.ui -o login_page.py')
    os.system('pyuic5 main_dialog.ui -o main_dialog.py')
    os.system('pyuic5 warning_dialog.ui -o warning_dialog.py')



# cd .\project\kiosk/ui
# python -m PyQt5.uic.pyuic -x main_ui.ui -o main_ui.py
