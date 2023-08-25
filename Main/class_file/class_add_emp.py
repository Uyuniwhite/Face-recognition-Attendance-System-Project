from Main.UI.AddEmployee import Ui_AddEmployee
from Main.class_file.class_warning_msg import MsgBox
from PyQt5.QtWidgets import QWidget

class AddEmpolyee(QWidget, Ui_AddEmployee):
    def __init__(self, controller):
        super().__init__()
        self.main = controller
        self.init_UI() # UI init
        self.init_func() # function init


    def init_UI(self):
        self.setupUi(self)
        self.set_data_cb()

        # 변수
        self.face_regist = False  # 얼굴인식 유/무

    def init_func(self):
        # 버튼 클릭 이벤트
        self.cancel_btn.clicked.connect(self.close)
        self.admit_btn.clicked.connect(self.clicked_add_empolyee_btn)

    def clicked_add_empolyee_btn(self):
        emp_name = self.name_lineedit.text()
        emp_dept = self.comboBox.currentIndex()
        emp_id = self.user_id_lineedit.text()
        emp_pw = self.pw_lineedit.text()
        emp_re_pw = self.pw_recheck_lineedit.text()

        result_name = self.verify_name(emp_name)
        result_id = self.verify_id(emp_id)
        result_pw = self.verify_pw(emp_pw, emp_re_pw)
        result_dept = self.convert_dept(emp_dept)

        msgbox = MsgBox() # 메시지박스 객체 생성
        message = ''
        print(f"result_name = {result_name}")
        print(type(result_name))
        if result_name == 0:
            message = "이름에 공백이 존재합니다!"
        elif result_name == 1:
            message = "이름이 8글자를 초과합니다!"
        elif result_name == 2:
            if result_id == 0:
                message = "ID에 공백이 존재합니다!"
            elif result_id == 1:
                message = "ID가 15자를 초과합니다!"
            elif result_id == 3:
                message = "중복된 ID가 존재합니다!"
            elif result_id == 2:
                if result_pw == 0:
                    message = "패스워드에 공백이 존재합니다!"
                elif result_pw == 1:
                    message = "패스워드가 20자를 초과합니다!"
                elif result_pw == 2:
                    message = "동일한 패스워드를 입력하세요!"
                elif result_pw == 3:
                    if not self.face_regist:
                        message = "얼굴 인식을 진행해주세요!"
                    elif self.face_regist:
                        message = "신규 사원 등록이 완료되었습니다!"

                        msgbox.set_dialog_type(type=1, msg=message)
                        msgbox.exec_()
                        return self.close()

        msgbox.set_dialog_type(type=1, msg=message)
        msgbox.exec_()

    # 이름 검증
    def verify_name(self, name):
        if len(name) == 0 or ' ' in name:
            return 0 # 이름 미입력 또는 스페이스 입력
        elif len(name) > 8:
            return 1 # 이름 8글자 초과
        else:
            return 2

    # 아이디 검증
    def verify_id(self, id_):
        if len(id_) == 0 or ' ' in id_:
            return 0 # 공백 유무
        elif len(id_) > 15:
            return 1 # 15자 초과
        else:
            duple_result = self.main.dbconn.id_duple_check(id_)
            print(f"중복검사 결과 {duple_result}")
            if duple_result:
                return 2
            elif not duple_result:
                return 3

    # 패스워드 검증
    def verify_pw(self, pw, re_pw):
        if len(pw) == 0 or ' ' in pw:
            return 0 # 패스워드 미입력 또는 스페이스 입력
        elif len(pw) > 20 :
            return 1 # 20자 초과
        else:
            if pw != re_pw:
                return 2 # 패스워드 2차 입력 다름
            else:
                return 3


    # 부서 텍스트를 부서 번호로 변경
    def convert_dept(self, dept):
        dept_id = (10 * dept) + 10
        print(dept_id)
        return dept_id

    # 얼굴 인식 관련
    def clicked_face_rec_btn(self):
        pass

    # 콤보박스 데이터 넣기
    def set_data_cb(self):
        dept_list = self.main.dbconn.find_dept()
        self.comboBox.addItems(dept_list)