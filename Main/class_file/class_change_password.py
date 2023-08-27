from Main.UI.PassWordChangeDialog import Ui_PWChangeDialog
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
        self.cancel_btn.clicked.connect(self.close) # 취소 버튼
        self.set_random_letter()
        self.pushButton.clicked.connect(self.set_random_letter)

    def create_random_str(self):
        random_num = string.digits
        random_ascii = string.ascii_letters
        random_letter = random_num + random_ascii
        random_sample = random.sample(random_letter, 6)
        random_choice = ''.join(random_sample)
        return random_choice

    def set_random_letter(self):
        letter = self.create_random_str()
        self.lineEdit_4.setText(letter)