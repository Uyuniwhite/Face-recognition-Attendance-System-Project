from Main.class_file.class_login import LoginFunc
from Main.class_file.class_dbconnect import DBconnect
from Main.class_file.class_main_page import MainPage
from Main.class_file.class_warning_msg import MsgBox
from Main.class_file.class_open_page import OpenPage
from Main.class_file.class_add_emp import AddEmpolyee
from Main.class_file.class_capture_user_img import CaptureUserImage
from Main.class_file.class_leave_work import CheckLeaveWork
from Main.class_file.class_show_out_img import ShowOutForWhile
from Main.class_file.class_check_out import CheckOutWhile


from PyQt5.QtWidgets import QWidget




class Controller(QWidget):
    def __init__(self):
        super().__init__()

        self.login = LoginFunc(self) # 로그인 페이지 객체 생성
        self.dbconn = DBconnect(self) # DB 커넥트 객체 생성
        self.main_page = MainPage(self) # 메인 페이지 객체 생성
        # self.msgbox = MsgBox(self) # 메세지박스 객체 생성
        self.open_page = OpenPage(self) # 오픈페이지 객체 생성
        self.add_emp = AddEmpolyee(self)  # 사원등록 객체 생성
        self.face_cap = CaptureUserImage(self, newbie_name=None) # 얼굴 캡쳐 객체 생성
        self.show_out_img = ShowOutForWhile(self) # 외출 중 표시 위젯 객체 생성
        self.check_out = CheckOutWhile(self) # 외출 복귀 확인 객체 생성
        self.leave_work = CheckLeaveWork(self) # 퇴근 확인 객체 생성
