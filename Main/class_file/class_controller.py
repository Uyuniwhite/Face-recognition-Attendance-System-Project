from Main.class_file.class_login import LoginFunc
from Main.class_file.class_dbconnect import DBconnect
from PyQt5.QtWidgets import QWidget
from Main.class_file.class_main_page import MainPage
from Main.class_file.class_warning_msg import MsgBox



class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.login = LoginFunc(self) # 로그인 페이지 객체 생성
        self.dbconn = DBconnect(self) # DB 커넥트 객체 생성
        self.main_page = MainPage(self) # 메인 페이지 객체 생성
        self.msgbox = MsgBox(self) # 메세지박스 객체 생성