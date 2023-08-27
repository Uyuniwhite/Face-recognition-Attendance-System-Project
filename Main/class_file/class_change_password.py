from Main.UI.PassWordChangeDialog import Ui_PWChangeDialog
from Main.class_file.class_warning_msg import MsgBox
from PyQt5.QtWidgets import QDialog
import random
import string


class PasswordChange(QDialog, Ui_PWChangeDialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)

        self.controller = controller

        self.init_UI()

    def init_UI(self):
        # 버튼 클릭 / 시그널
        self.cancel_btn.clicked.connect(self.close)  # 취소 버튼
        self.user_id = None  # user id 더미 생성
        self.letter = None  # 자동입력방지문자 더미생성
        self.set_random_letter()  # 자동입력방지문자 settext
        self.pushButton.clicked.connect(self.set_random_letter)  # 자동입력방지 문자 새로고침 버튼 이벤트
        self.ok_btn.clicked.connect(self.clicked_ok_btn)

    # 자동입력방지 문자 랜덤생성 ( 숫자 + 소문자 + 대문자)
    def create_random_str(self):
        random_num = string.digits
        random_ascii = string.ascii_letters
        random_letter = random_num + random_ascii
        random_sample = random.sample(random_letter, 6)
        random_choice = ''.join(random_sample)
        return random_choice

    # 자동입력방지 문자 세팅
    def set_random_letter(self):
        self.letter = self.create_random_str()
        self.lineEdit_4.setText(self.letter)

    # 확인 버튼 클릭 이벤트
    def clicked_ok_btn(self):
        result_current_pw = self.vertify_current_pw()
        result_new_pw = self.verify_new_pw()
        result_letter = self.verify_random_letter()
        msgbox = MsgBox()
        message = str()

        if not result_current_pw:
            message = "현재 비밀번호가 다릅니다!"
        elif not result_new_pw:
            message = "새 비밀번호를 입력하지 않았거나 공백이 존재합니다!"
        elif result_new_pw == 'long':
            message = "새 비밀번호가 20자를 초과합니다!"
        elif result_new_pw == 'different':
            message = "동일한 새 비밀번호를 입력해주세요!"
        elif not result_letter:
            message = "자동입력방지문자를 확인하세요!"
        else:
            message = "비밀번호가 변경되었습니다!"
            new_pw = self.new_pw_edit.text()
            self.controller.dbconn.save_new_pw(self.user_id, new_pw)
            msgbox.set_dialog_type(msg=message, img='warn')
            msgbox.exec_()
            self.close()
            return

        msgbox.set_dialog_type(msg=message, img='warn')
        msgbox.exec_()

    # 현재 비밀번호 검증
    def vertify_current_pw(self):
        current_pw = self.lineEdit.text()
        db_pw = self.controller.dbconn.get_current_pw(self.user_id)
        if current_pw != db_pw:
            return False  # 현재 비밀번호 일치하지 않음
        else:
            return True  # 현재 비밀번호 일치

    # 새로운 비밀번호 검증
    def verify_new_pw(self):
        new_pw = self.new_pw_edit.text()
        re_new_pw = self.new_pw_recheck_edit.text()

        if len(new_pw) == 0 or ' ' in new_pw:
            return False  # 미입력 또는 공백 존재
        elif len(new_pw) > 20:
            return 'long'  # 길이 초과
        elif new_pw != re_new_pw:
            return 'different'  # 새로운 비밀번호 다름
        else:
            return True  # 이상없으면 True 리턴

    # 자동입력방지문자 검증
    def verify_random_letter(self):
        input_letter = self.lineEdit_5.text()

        if self.letter != input_letter:
            return False  # 자동입력방지 검증 실패
        else:
            return True  # 자동입력방지 검증 성공
