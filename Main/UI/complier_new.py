# import subprocess

# def compile_ui(ui_files, py_files):
#     for ui_file, py_file in zip(ui_files, py_files):
#         command = f"python -m PyQt5.uic.pyuic -x {ui_file} -o {py_file}"
#         subprocess.run(command, shell=True)
#
# if __name__ == "__main__":
#
#     ui_files = ['LoginWidget.ui', 'MainWidget.ui', 'warning_dialog.ui', 'OpenWidget.ui']
#
#     py_files = ['LoginWidget.py', 'MainWidget.py', 'warning_dialog.py' 'OpenWidget.py']
#
#     compile_ui(ui_files, py_files) # 여러 파일 컴파일
#     print('컴파일러 완료!')


import os
import sys

if __name__ == '__main__':
    os.system(f"pyrcc5 ../../img/icon/resource.qrc -o resource.py")

    uis = ['LoginWidget', 'MainWidget', 'warning_dialog', 'OpenWidget',
           'UserCell', 'AddEmployee', 'SaveUserImg', 'PassWordChangeDialog',
           'ShowGraph', 'Opening']
    for ui in uis:
        os.system(f'python  -m PyQt5.uic.pyuic --import-from=Main.UI -x {ui}.ui -o {ui}.py')
    print('컴파일 완료!')