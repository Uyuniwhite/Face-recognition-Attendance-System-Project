from class_login_2 import LoginFunc
from PyQt5.QtWidgets import QWidget
from class_main_page import MainPage


class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.login = LoginFunc(self)  # 로그인 페이지 객체 생성
        self.main_page = MainPage(self)