from Main.UI.warning_dialog import Ui_WarningDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from Main.class_file.class_font import Font


class MsgBox(QDialog, Ui_WarningDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 투명하게 함
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 클릭 이벤트
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        # 폰트 설정
        self.warn_lab.setFont(Font.text(2))
        self.ok_btn.setFont(Font.text(2, weight='bold'))
        self.cancel_btn.setFont(Font.text(2, weight='bold'))

        # 커서 설정
        self.setCursor(QCursor(QPixmap('../../img/icon/cursor_1.png').scaled(40, 40)))

    # 취소 눌렀을 때
    def reject(self):
        self.setResult(0)
        super(MsgBox, self).reject()

    # 확인 눌렀을 때
    def accept(self):
        self.setResult(1)
        super(MsgBox, self).accept()

    ''' 
    메세지박스 사용 방법
    msgbox = MsgBox()
    msgbox.set_dialog_type(type=1, msg="샘플 메시지", img='warn')
    msgbox.exec_()  # 메시지박스 실행
    
    if msgbox.result() == 1:
        print("OK 버튼을 눌렀습니다!")
    elif msgbox.result() == 0:
        print("Cancel 버튼을 눌렀습니다!")
    '''

    def set_dialog_type(self, type="", msg="", img='warn'):

        import os
        # 작업 디렉토리를 현재 스크립트의 디렉토리로 변경
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # 기본 설정
        self.cancel_btn.setVisible(False)

        # 커서 설정
        self.setCursor(QCursor(QPixmap('../../img/icon/cursor_1.png').scaled(40, 40)))

        # 이미지 경로 설정
        img_path_dict = {
            'check': "../../img/icon/check.png",
            'password': '../../img/icon/password.png',
            'warn': '../../img/icon/warning-sign.png',
            'camera': '../../img/icon/camera.png',
            'delete': '../../img/icon/trash.png'

        }
        relative_path = img_path_dict[img]
        absolute_path = os.path.abspath(relative_path)

        if type == 1:
            msg = "아이디 또는 패스워드를 확인하세요!"
        elif type == 2:
            msg = '등록된 사원이 아닙니다!'
        elif type == 3:
            msg = "패스워드가 일치하지 않습니다!"
        elif type == 4:
            self.cancel_btn.setVisible(True)

        self.warn_lab.setText(msg)
        self.icon_lab.setScaledContents(True)
        self.icon_lab.setPixmap(QPixmap(absolute_path))
