from Main.UI.AddEmployee import Ui_AddEmployee
from Main.class_file.class_warning_msg import MsgBox
from PyQt5.QtWidgets import QWidget

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

    def btn_event(self):
        self.cancel_btn.clicked.connect(self.close) # 창 닫기
        self.admit_btn.clicked.connect(self.clicked_admit_btn)

    def set_emp_info(self):
        user_info = self.controller.dbconn.get_user_data(self.emp_id)
        user_name, user_id, user_pw, dept_id = user_info[1:]

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


    def set_data_cb(self):
        dept_list = self.controller.dbconn.find_dept()
        self.comboBox.addItems(dept_list)

    def current_dept_name(self, dept_name):
        idx = self.comboBox.findText(dept_name)
        self.comboBox.setCurrentIndex(idx)

    def clicked_admit_btn(self):
        new_dept_name = self.comboBox.currentText()
