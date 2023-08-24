from class_login import LoginFunc
from PyQt5.QtWidgets import QWidget


class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.login = LoginFunc(self)  # 로그인 페이지 객체 생성
