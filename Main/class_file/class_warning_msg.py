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
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 클릭 이벤트
        self.ok_btn.clicked.connect(self.close)
        self.cancel_btn.clicked.connect(self.close)

        # 폰트 설정
        self.warn_lab.setFont(Font.text(2))
        self.ok_btn.setFont(Font.text(2, weight='bold'))
        self.cancel_btn.setFont(Font.text(2, weight='bold'))

        # 커서 설정
        self.setCursor(QCursor(QPixmap('../img/icon/cursor_1.png').scaled(40, 40)))

    # # 아니오, 닫기 눌렀을 때
    # def reject(self) -> None:
    #     self.setResult(0)
    #     self.close()
    #
    # # 예, 확인 눌렀을 때
    # def accept(self) -> None:
    #     self.setResult(1)
    #     self.close()

    def set_dialog_type(self, type="", msg=""):

        import os
        # 작업 디렉토리를 현재 스크립트의 디렉토리로 변경
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # 기본 설정
        self.cancel_btn.hide()
        relative_path = "../../img/icon/check.png"

        if type == 1:
            relative_path = "../../img/icon/check.png"
        if type == 2:
            relative_path = '../../img/icon/password.png'

            msg = '얼굴인식이 어렵습니다. \n ' \
                  '아이디와 비밀번호로 로그인 해 주세요!'

        if type == 3:
            self.cancel_btn.show()
            msg = '해당 유저를 삭제하시겠습니까?'

        if type == 4:
            msg = f"등록된 사원이 아닙니다!"
        if type == 5:
            msg = f"500장의 사진을 찍습니다.\n다양한 각도에서 사진을 찍어주세요."
            relative_path = '../../img/icon/camera.png'
        if type == 6:
            msg = f"[오류!]\n이미지 캡쳐에 실패했습니다."
            relative_path = '../../img/icon/warning-sign.png'

        absolute_path = os.path.abspath(relative_path)

        self.warn_lab.setText(msg)
        self.icon_lab.setScaledContents(True)
        self.icon_lab.setPixmap(QPixmap(absolute_path))
