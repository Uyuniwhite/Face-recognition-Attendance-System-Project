import psycopg2
from  datetime import datetime
host = "10.10.20.103"
port = "5432"
database = "ATD"
name = "postgres"
password = "1234"

class DBconnect:
    def __init__(self, controller):
        self.controller = controller
        self.conn = None
        self.cur = None
        # self.start_conn()
    def start_conn(self):
        self.conn = psycopg2.connect(host=host, database=database, user=name, password=password, port=port)
        self.cur = self.conn.cursor()

        return self.cur

    def commit_db(self):
        if self.conn is not None:
            self.conn.commit()

    def end_conn(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    # 출근 데이터 저장
    def log_in(self, user_id, day_date, time_date, login_type):
        user_no = self.find_no(user_id)
        clock_in = self.clock_in_check(user_no, day_date) # 출근 여부 출근 안했으면 0, 했으면 1
        c = self.start_conn()
        if user_no != None:
            if clock_in == 0:
                clock_in_query = "insert into tb_atd (user_no, atd_date, atd_time, atd_start, atd_end, atd_type, atd_leave) " \
                                 f"values('{user_no}', '{day_date}','{time_date}',1,0,'{login_type}', 'NULL')"
                c.execute(clock_in_query)
                self.commit_db()
                self.end_conn()
                return True
        else:
            self.end_conn()
            return False # 등록된 사원이 아니면 False를 리턴함


    # user_no 찾는 함수
    def find_no(self, user_id):
        c = self.start_conn()
        no_query = f"select user_no from tb_user where user_id = '{user_id}'"
        # no_query = f"select tb_user.user_no from tb_user join tb_atd on tb_user.user_no = tb_atd.user_no " \
        #            f"where tb_user.user_id = '{user_id}' and tb_atd.atd_date = '{day_date}'"  # user_no 찾는 쿼리
        c.execute(no_query)  # user_no 찾는 쿼리문 실행
        data = c.fetchone()  # user_no
        if data != None:
            self.end_conn()
            return data[0]
        else:
            self.end_conn()
            return None

    from datetime import datetime

    def return_datetime(self, type):
        """원하는 날짜/시간 포멧을 반환"""
        now = datetime.now()  # 시간

        if type == 'date':
            now_format = now.strftime("%Y-%m-%d")  # 년 월 일
        elif type == 'time':
            now_format = now.strftime("%Y-%m-%d %H:%M:%S")  # 년 월 일 시 분 초
        elif type == 'time_only':
            now_format = now.strftime("%H:%M:%S")  # 시 분 초
        elif type == 'year_month':
            now_format = now.strftime("%Y-%m")  # 년월
        elif type == 'c_date':
            now_format = now.strftime("%d")  # 일
        else:
            return "Invalid type"

        # print('[dateimte.py]시간 포멧팅: ', now_format)
        return now_format

    def return_specific_data(self, column, table_name, condition=None, type=1):
        """특정 열 데이터만 반환합니다."""
        c = self.start_conn()

        query = f"SELECT {column} FROM {table_name}"
        if condition is not None:
            query += f" WHERE {condition}"
        print(query)

        c.execute(query)
        r_data = c.fetchall()
        # print('데이터', r_data)

        if type == 1:
            return r_data[0][0]
        return r_data

    def return_user_atd_info(self, user_id, year_month):
        c = self.start_conn()
        user_no = self.find_no(user_id=user_id) # 유저 아이디 반환

        query = f"select * from tb_atd where user_no = {user_no} and atd_date like '%{year_month}%'";
        c.execute(query)
        r_data = c.fetchall()

        print(r_data)
        return r_data

    def return_user_atd_month(self, user_id):
        """유저가 출근한 월들만 리스트로 반환"""
        user_no = self.find_no(user_id) # 유저 번호 반환
        result = self.return_specific_data(column='atd_date', table_name='tb_atd', condition=f'user_no={user_no}', type=2) # 유저 출근 날들 반환

        result = [date[0][:7] for date in result] # 출근 년도 - 월수만 반환
        unique_result = []
        [unique_result.append(x) for x in result if x not in unique_result] # 그 중 중복값 제거

        print(unique_result)
        return unique_result

    def return_user_atd_summary(self, user_id):
        # 유저 이름
        con = f"user_id = '{user_id}'"  # 조건1
        user_name = self.return_specific_data(column='user_name', table_name='tb_user', condition=con)

        # 현재 년-월
        current_year_month = self.return_datetime(type='year_month')
        current_date = self.return_datetime(type='c_date')

        # 유저 번호
        user_no = self.dbconn.find_no(user_id)

        # 출근일수
        con2 = f"user_no = {user_no} and atd_date like '%{current_year_month}%'"  # 조건2
        user_atd_day = self.return_specific_data(column='count(*)', table_name='tb_atd',
                                                                   condition=con2, type=1)
        # 근태율 계산 = (현재 달 출근일 / 현재 달 날짜) * 100
        atd_per = round((int(user_atd_day) / int(current_date)) * 100, 2)
        text = f'{user_name}님의 {current_year_month[-2:]}월 출근일수는 {user_atd_day}일, 근태율은 {atd_per}%입니다.'

        return text

    # def return_all_data(self, table_name, condition=None):
    #     c = self.start_conn()
    #     query = f"SELECT {column} FROM {table_name}"



    # 출근 여부 확인
    def clock_in_check(self, user_no, day_date):
        c = self.start_conn()
        check_query = f"select atd_start from tb_atd join tb_user on tb_atd.user_no = tb_user.user_no " \
                      f"where tb_atd.user_no = '{user_no}' and tb_atd.atd_date = '{day_date}'"
        c.execute(check_query)
        data = c.fetchone()
        if data != None:
            return data[0]
        else:
            return 0
        self.end_conn()

    def regiseter_info(self):
        c = self.start_conn()

    # 부서 목록 이름만 담아서 리스트로 반환
    def find_dept(self):
        dept_list = list()
        c = self.start_conn()
        dept_query = "select dept_name from tb_dept group by dept_name"
        c.execute(dept_query)
        datas = c.fetchall()
        for data in datas:
            name = data[0]
            dept_list.append(name)

        return dept_list

    # 부서명, 부서코드, 부서인원수 리턴해주기
    def info_dept(self):
        c = self.start_conn()
        dept_query = "select tb_dept.dept_id, tb_dept.dept_name, count(*) from tb_dept " \
                     "join tb_user on tb_dept.dept_id = tb_user.dept_id group by tb_dept.dept_id, tb_dept.dept_name"
        c.execute(dept_query)
        data = c.fetchall()
        self.end_conn()
        return data


    # 선택한 부서별 사원만 리스트 담아서 리턴
    def select_dept(self, dept):
        empolyee_list = list()
        c = self.start_conn()
        empolyee_query = "select tb_user.user_name, tb_user.user_id, tb_dept.dept_name from tb_user join tb_dept on tb_user.dept_id = tb_dept.dept_id " \
                         f"where tb_dept.dept_name = '{dept}'"
        c.execute(empolyee_query)
        datas = c.fetchall()
        for data in datas:
            empolyee_list.append(data)

        return empolyee_list

    # DB에서 아이디 / 패스워드 검증
    def check_id_pw(self, user_id):
        c = self.start_conn()
        check_query = f"select user_pw from tb_user where user_id = '{user_id}'"
        c.execute(check_query)
        pw = c.fetchone()

        if pw == None:
            return False # 등록된 아이디 없음
        else:
            return pw[0]

    # 관리자 사원 등록 아이디 중복검사
    def id_duple_check(self, user_id):
        c = self.start_conn()
        query = f"select * from tb_user where user_id = '{user_id}'"
        c.execute(query)
        result = c.fetchone()
        if result != None:
            return False # 중복된 아이디
        else:
            return True # 중복 통과

    # 신규 사원 등록
    def save_newbie(self, newbie_name, newbie_id, newbie_pw, dept_id):
        c = self.start_conn()
        add_query = "insert into tb_user (user_name, user_id, user_pw, dept_id) values " \
                    f"('{newbie_name}', '{newbie_id}', '{newbie_pw}', '{dept_id}')"
        c.execute(add_query)
        self.commit_db()
        self.end_conn()

    # 사원 삭제
    def delete_empolyee(self, emp_id):
        c = self.start_conn()
        del_query = f"delete from tb_user where user_id = '{emp_id}'"
        c.execute(del_query)
        self.commit_db()
        self.end_conn()

    # 퇴근 기록 DB 저장 코드
    def leave_workplace(self, user_id, day_date, time_date):
        user_no = self.find_no(user_id)
        c = self.start_conn()
        leave_query = f"update tb_atd set atd_end = 1, atd_leave = '{time_date}' " \
                      f"where user_no = '{user_no}' and atd_date = '{day_date}' and atd_end = 0"
        c.execute(leave_query)
        self.commit_db()
        self.end_conn()


if __name__ == '__main__':
    db_conn = DBconnect(controller=None)
    # db_conn.return_user_atd_info(user_id='soyeon',year_month='2023-08')
    db_conn.return_user_atd_month(user_id='soyeon')


