from Main.class_file.class_login import LoginFunc
from Main.class_file.class_dbconnect import DBconnect
from PyQt5.QtWidgets import QWidget




class Controller(QWidget):
    def __init__(self):
        super().__init__()
        self.login = LoginFunc(self) # 로그인 페이지 객체 생성
        self.dbconn = DBconnect(self) # DB 커넥트 객체 생성