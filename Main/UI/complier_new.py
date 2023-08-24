import subprocess

def compile_ui(ui_files, py_files):
    for ui_file, py_file in zip(ui_files, py_files):
        command = f"python -m PyQt5.uic.pyuic -x {ui_file} -o {py_file}"
        subprocess.run(command, shell=True)

if __name__ == "__main__":

    ui_files = ['LoginWidget.ui', 'MainWidget.ui', 'warning_dialog.ui']

    py_files = ['LoginWidget.py', 'MainWidget.py', 'warning_dialog.py']

    compile_ui(ui_files, py_files) # 여러 파일 컴파일
    print('컴파일 완료!')