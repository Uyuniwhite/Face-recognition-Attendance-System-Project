from Main.UI.AddEmployee import Ui_AddEmployee
from Main.class_file.class_warning_msg import MsgBox
from Main.class_file.class_font import Font
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtCore import Qt
import os

class DeptChange(QWidget, Ui_AddEmployee):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.controller = controller
        self.emp_id = None
        self.init_UI()

    def init_UI(self):
        self.emp_add_title.setText("사원 정보")
        self.admit_btn.setText('변경')
        self.face_rec_btn.setVisible(False)
        self.btn_event()
        # line edit set readonly
        self.name_lineedit.setReadOnly(True)
        self.pw_lineedit.setReadOnly(True)
        self.user_id_lineedit.setReadOnly(True)
        self.pw_recheck_lineedit.setReadOnly(True)
        self.set_font()
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 현재 위치
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # 이미지 넣기
        self.setCursor(QCursor(QPixmap('../../img/icon/cursor_1.png').scaled(40, 40)))

    def set_font(self):
        self.emp_add_title.setFont(Font.title(2))
        self.dept_lab.setFont(Font.button(1))
        self.user_id_lab.setFont(Font.button(1))
        self.name_lab.setFont(Font.button(1))
        self.pw_lab.setFont(Font.button(1))
        self.pw_recheck_lab.setFont(Font.button(1))

        self.admit_btn.setFont(Font.button(1))
        self.face_rec_btn.setFont(Font.button(1))
        self.cancel_btn.setFont(Font.button(1))

        self.name_lineedit.setFont(Font.text(1, weight='light'))
        self.comboBox.setFont(Font.text(1, weight='light'))
        self.user_id_lineedit.setFont(Font.text(1, weight='light'))
        self.pw_lineedit.setFont(Font.text(1, weight='light'))
        self.pw_recheck_lineedit.setFont(Font.text(1, weight='light'))


    def btn_event(self):
        self.cancel_btn.clicked.connect(self.close) # 창 닫기
        self.admit_btn.clicked.connect(self.clicked_admit_btn)

    def set_emp_info(self):
        user_info = self.controller.dbconn.get_user_data(self.emp_id)
        user_name, user_id, user_pw, dept_id = user_info[1:5]

        dept_name = self.convert_dept_id_tostring(dept_id)
        self.name_lineedit.setText(user_name)
        self.user_id_lineedit.setText(user_id)
        self.pw_lineedit.setText(user_pw)
        self.pw_recheck_lineedit.setText(user_pw)

        self.set_data_cb()
        self.current_dept_name(dept_name)

    def convert_dept_id_tostring(self, dept_id):
        dept_data = {10:'개발부', 20:'인사팀', 30:'회계팀', 40:'감사팀', 50:'영업팀'}
        dept_name = dept_data[dept_id]
        return dept_name

    def convert_dept_name_int(self, dept_name):
        dept_data = {10: '개발부', 20: '인사팀', 30: '회계팀', 40: '감사팀', 50: '영업팀'}
        dept_id = int()

        for key, value in dept_data.items():
            if value == dept_name:
                dept_id = key
                return dept_id

    def set_data_cb(self):
        dept_list = self.controller.dbconn.find_dept()
        self.comboBox.clear()
        self.comboBox.addItems(dept_list)

    def current_dept_name(self, dept_name):
        idx = self.comboBox.findText(dept_name)
        self.comboBox.setCurrentIndex(idx)

    def clicked_admit_btn(self):
        new_dept_name = self.comboBox.currentText()
        dept_id = self.convert_dept_name_int(new_dept_name)
        user_id = self.user_id_lineedit.text()

        txt = "변경하시겠습니까?"
        result = self.msgbox_obj(4, txt, img='question')
        if result == 1:
            self.controller.dbconn.update_dept_id(user_id, dept_id)
            txt = "변경 완료됐습니다!"
            self.msgbox_obj("", txt, img='check')
            self.close()
        elif result == 0:
            txt = "취소했습니다!"
            self.msgbox_obj("",txt, img='check')


    def msgbox_obj(self,type, txt, img):
        msgbox = MsgBox()
        message = txt
        msgbox.set_dialog_type(type=type, msg=message, img=img)
        msgbox.exec_()
        result = msgbox.result()
        return result



