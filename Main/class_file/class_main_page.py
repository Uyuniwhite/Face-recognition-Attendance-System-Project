from Main.UI.MainWidget import Ui_MainWidget
from Main.class_file.class_user_cell import UserCell
from Main.class_file.class_font import Font
from Main.class_file.class_warning_msg import MsgBox
from Main.class_file.class_show_graph import ShowGraph
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap, QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.colors
from scipy.interpolate import interp1d
import numpy as np
import os


class MainPage(QWidget, Ui_MainWidget):
    SetUserId = pyqtSignal(str)

    def __init__(self, controller):
        super().__init__()

        # 컨트롤러 가져오기
        self.controller = controller

        # 유저 Id
        self.user_id = None

        self.setupUi(self)
        self.initUI()  # 기본 설정
        self.initStyle()  # 스타일 설정
        self.msgbox = MsgBox()  # 메세지박스 객체 싱성

    def initUI(self):
        self.stackedWidget.setCurrentWidget(self.home_page) # 초기화면 홈페이지로 설정
        # 페이지 이동
        # self.home_btn.clicked.connect(
        #     lambda x: self.stackedWidget.setCurrentWidget(self.home_page))  # 관리자일 경우에는 팀 관리 화면으로 넘어가게 하기
        self.home_btn.clicked.connect(self.move_homepage)
        self.atd_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.atd_page))  # 근태관리 페이지 이동
        self.mypage_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.my_page))  # 마이페이지 이동

        # 버튼 클릭 이벤트
        self.add_btn.clicked.connect(self.add_employee)  # 사원 추가 버튼 클릭시
        self.team_search_btn.clicked.connect(self.set_grid_lay)  # 팀 검색 버튼 눌렀을 때
        self.out_btn.clicked.connect(self.show_out_while_img)  # 외출하기 버튼 클릭
        self.end_btn.clicked.connect(self.clicked_end_btn)  # 퇴근하기 버튼 클릭
        # self.attend_check_btn.clicked.connect(lambda x, y=self.user_id: self.show_atd_table(user_id=y))  # 특정 달 출근일자 테이블에 보여주기
        self.SetUserId.connect(self.set_user_id)
        self.mypage_btn.clicked.connect(self.get_userinfo_from_DB)  # 마이페이지 데이터 반영 관련
        self.edit_btn.clicked.connect(self.clicked_edit_btn)
        self.dept_tablewidget.cellDoubleClicked.connect(self.get_tbwid_data)  # 테이블 위젯 셀 클릭 이벤트
        self.dept_tablewidget.setSelectionMode(QTableWidget.NoSelection)  # 셀 클릭시 블록 설정 안되게
        self.emp_detail_check.clicked.connect(self.check_emp_info)  # 관리자 사원 정보 확인 버튼 클릭
        self.back_to_dept_btn.clicked.connect(self.clicked_back_btn)  # 관리자 사원관리 뒤로가기 버튼 이벤트
        self.graph_widget_1.mousePressEvent = self.show_large_graph
        self.graph_widget_2.mousePressEvent = self.show_large_bar_graph
        self.graph_widget_3.mousePressEvent = self.show_large_admin_bar_graph
        self.graph_widget_4.mousePressEvent = self.show_large_admin_donut_graph

        # 부서 콤보박스에 넣기
        self.team_search_combobox.clear()
        depts = self.controller.dbconn.find_dept()
        self.team_search_combobox.addItems(depts)

        # 테이블 채우기
        self.set_dept_table()


    # 디버깅 해야 함(로그인 후 user_id)가 변경이 안되는 현상이 생김
    def show_atd_table(self, user_id):
        if user_id is not None:
            current_month = self.attend_check_combobox.currentText()
            atd_list = self.controller.dbconn.return_user_atd_info(user_id=user_id, year_month=current_month)
            print('오류나는 곳', atd_list)
            self.set_graph_for_user(atd_list)
            self.tableWidget.setRowCount(len(atd_list))
            self.tableWidget.setColumnCount(6)

            for idx, data in enumerate(atd_list):
                date, start_time, end_time, atd_type = data[1], data[2], data[7], data[5]
                date_day = self.controller.dbconn.get_day_of_week(text_date=date)
                if end_time != 'NULL':
                    time_difference = self.controller.dbconn.get_strptime(start_time, end_time)
                else:
                    time_difference = '근무중'
                if atd_type == 'face':
                    atd_type = '얼굴인식'

                # 각 아이템을 생성하고 가운데 정렬한 후, 테이블에 추가
                for col, value in enumerate([date, date_day, start_time, atd_type, end_time, time_difference]):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
                    self.tableWidget.setItem(idx, col, item)

            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            header = self.tableWidget.horizontalHeader()  # 수평 헤더 (컬럼 헤더) 가져오기
            header.setFont(Font.button(1))
    def set_user_id(self, user_id):
        """로그인 할 때 유저 아이디가 변경됨"""
        self.user_id = user_id
        self.attend_check_btn.clicked.connect(lambda x, y=self.user_id: self.show_atd_table(user_id=y))

    # 유저 출근 달들만 리턴
    def set_user_atd_combo(self, user_id):
        user_atd_months = self.controller.dbconn.return_user_atd_month(user_id=user_id)
        self.attend_check_combobox.addItems(user_atd_months)

    # 근태화면 하단 요약 부분
    def set_user_atd_summary(self, user_id):
        text, user_atd_day, atd_per, absent_day = self.controller.dbconn.return_user_atd_summary(user_id=user_id)
        self.summary_lab.setText(text)
        self.atd_per_lab.setText(f"{str(atd_per)[:2]}%")
        self.attend_day_lab.setText(f'{str(user_atd_day)}일')
        self.out_day_lab.setText(f'{str(absent_day)}일')

    # 외출하기 버튼 클릭시
    def show_out_while_img(self):
        self.msgbox.set_dialog_type(type=5, img='question')
        self.msgbox.exec_()
        if self.msgbox.result() == 1:
            self.controller.show_out_img.show()

    # 퇴근하기 버튼 클릭시
    def clicked_end_btn(self):
        self.msgbox.set_dialog_type(type=6, img='question')
        self.msgbox.exec_()
        if self.msgbox.result() == 1:
            self.controller.leave_work.show()

    def initStyle(self):
        # 현재 위치
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # 이미지 넣기
        self.setCursor(QCursor(QPixmap('../../img/icon/cursor_1.png').scaled(40, 40)))
        self.img_lab.setPixmap(QPixmap('../../img/icon/user.png').scaled(60, 60))
        self.back_to_dept_btn.setIcon(QIcon('../../img/icon/back.png'))
        self.back_to_dept_btn.setIconSize(QSize(40, 40))

        # 폰트 설정
        self.set_font()
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False

    # 사원 추가 버튼
    def add_employee(self):
        self.controller.add_emp.show()

    # 폰트 설정
    def set_font(self):
        """폰트 지정"""
        font_style_1 = Font.text(1)

        # 상단버튼
        self.home_btn.setFont(Font.button(6))
        self.atd_btn.setFont(Font.button(6))
        self.mypage_btn.setFont(Font.button(6))
        self.users_btn.setFont(Font.button(6))

        # 마이페이지
        self.name_lab.setFont(font_style_1)
        self.dept_lab.setFont(font_style_1)
        self.user_id_lab.setFont(font_style_1)
        self.pw_lab.setFont(font_style_1)
        self.pw_recheck_lab.setFont(font_style_1)

        self.edit_btn.setFont(Font.button(6))

        self.name_lineedit.setFont(font_style_1)
        self.dept_lineedit.setFont(font_style_1)
        self.user_id_lineedit.setFont(font_style_1)
        self.pw_lineedit.setFont(font_style_1)
        self.pw_recheck_lineedit.setFont(font_style_1)

        # 근태화면
        self.attend_check_lab.setFont(Font.text(0, weight='bold'))
        self.attend_check_combobox.setFont(Font.text(0))
        self.attend_check_btn.setFont(Font.text(0, weight='bold'))
        self.emp_detail_check.setFont(Font.text(0, weight='bold'))
        self.summary_lab.setFont(Font.button(7))

        # 메인 페이지
        self.attend_day_lab.setFont(Font.title(3))
        self.out_day_lab.setFont(Font.title(3))
        self.atd_per_lab.setFont(Font.title(3))
        self.dept_title.setFont(Font.title(6))

        self.attend_text_lab.setFont(Font.text(1))
        self.out_text_lab.setFont(Font.text(1))
        self.atd_per_text_lab.setFont(Font.text(1))

        self.out_btn.setFont(Font.text(4))
        self.end_btn.setFont(Font.text(4))

        self.home_name_lab.setFont(Font.text(2))
        self.home_dept_lab.setFont(Font.text(2))
        self.graph_contents_1.setFont(Font.text(4))
        self.graph_contents_2.setFont(Font.text(4))
        self.graph_contents_3.setFont(Font.text(4))
        self.graph_contents_4.setFont(Font.text(4))

        # 관리자 페이지
        self.team_search_lab.setFont(Font.text(1, weight='bold'))
        self.team_search_btn.setFont(Font.text(1, weight='bold'))
        self.add_btn.setFont(Font.text(1, weight='bold'))
        self.team_search_combobox.setFont(Font.text(1))

    def set_grid_lay(self):
        """그리드 영역에 위젯 클래스 넣어주기"""
        self.clear_layout(self.users_grid_lay)  # 그리드 레이아웃 클리어

        current_dept = self.team_search_combobox.currentText()
        empolyee_list = self.controller.dbconn.select_dept(current_dept)

        # 행의 개수를 원소 수에 따라 결정
        num_rows = (len(empolyee_list) // 3 + 1)  # 올림 계산을 사용하여 행의 개수를 결정

        cnt = 0

        # 그리드 레이아웃에 유저셀 넣어주기
        for i in range(num_rows):
            for j in range(3):  # 열은 3개로 고정
                if cnt < len(empolyee_list):  # test_list의 원소 수를 초과하지 않도록 함
                    # print(empolyee_list[cnt][0], empolyee_list[cnt][1])
                    user_cell = UserCell(self.controller, self, type=1, name=empolyee_list[cnt][0],
                                         user_id=empolyee_list[cnt][1])
                    self.users_grid_lay.addWidget(user_cell, i, j)
                    cnt += 1

    def clear_layout(self, layout: QLayout):
        """레이아웃 안의 모든 객체를 지웁니다."""
        if layout is None or not layout.count():
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
            # 아이템이 레이아웃일 경우 재귀 호출로 레이아웃 내의 위젯 삭제
            else:
                self.clear_layout(item.layout())

    def set_dept_table(self):
        dept_list_test = self.controller.dbconn.info_dept()
        self.dept_tablewidget.setRowCount(len(dept_list_test))
        self.dept_tablewidget.setColumnCount(4)

        for idx, data in enumerate(dept_list_test):
            dept_code, dept_name, dept_emp = data
            dept_atd_per = self.controller.dbconn.return_team_atd_per_for_table(dept_name)

            # 각 항목 생성 및 중앙 정렬
            item_dept_name = QTableWidgetItem(dept_name)
            item_dept_name.setTextAlignment(Qt.AlignCenter)
            self.dept_tablewidget.setItem(idx, 0, item_dept_name)

            item_dept_code = QTableWidgetItem(f'{dept_code}')
            item_dept_code.setTextAlignment(Qt.AlignCenter)
            self.dept_tablewidget.setItem(idx, 1, item_dept_code)

            item_dept_emp = QTableWidgetItem(f"{dept_emp}")
            item_dept_emp.setTextAlignment(Qt.AlignCenter)
            self.dept_tablewidget.setItem(idx, 2, item_dept_emp)

            item_dept_rate = QTableWidgetItem(f'{str(dept_atd_per)}%')
            item_dept_rate.setTextAlignment(Qt.AlignCenter)
            self.dept_tablewidget.setItem(idx, 3, item_dept_rate)

        self.dept_tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        header = self.dept_tablewidget.horizontalHeader()  # 수평 헤더 (컬럼 헤더) 가져오기
        header.setFont(Font.button(3))

    # DB에서 데이터 user 데이터 가져와서 마이페이지에 데이터 반영
    def get_userinfo_from_DB(self):
        user_data = self.controller.dbconn.get_user_data(self.user_id)
        user_name = user_data[1]
        user_id = user_data[2]
        user_pw = user_data[3]
        dept_id = user_data[-2]
        dept_name = self.convert_dept_id_to_name(dept_id)
        self.set_userinfo_mypage(user_name, user_id, user_pw, dept_name)

    # 마이페이지 개인정보 넣기
    def set_userinfo_mypage(self, user_name, user_id, user_pw, dept_name):
        self.name_lineedit.setText(user_name)
        self.dept_lineedit.setText(dept_name)
        self.user_id_lineedit.setText(user_id)
        self.pw_lineedit.setText(user_pw)
        self.pw_recheck_lineedit.setText(user_pw)

    # 부서 번호를 부서 이름으로 변환
    def convert_dept_id_to_name(self, dept_id):
        dept_info = {10: "개발팀", 20: "인사팀", 30: "회계팀", 40: "감사팀", 50: "영업팀"}
        dept_name = dept_info[dept_id]
        return dept_name

    def clicked_edit_btn(self):
        self.controller.pw_change.user_id = self.user_id
        self.controller.pw_change.exec()

    # 관리자모드에서 부서관리 테이블위젯 데이터 가져오기
    def get_tbwid_data(self, row, col):
        dept_name = self.dept_tablewidget.item(row, 0).text()
        self.stackedWidget.setCurrentWidget(self.admin_home_page)
        idx = self.team_search_combobox.findText(dept_name)
        self.team_search_combobox.setCurrentIndex(idx)
        self.team_search_btn.click()

    # 홈버튼 이벤트
    def move_homepage(self):
        if self.user_id == 'admin':
            self.stackedWidget.setCurrentWidget(self.admin_dept_check)
            self.set_dept_table()
        else:
            self.stackedWidget.setCurrentWidget(self.home_page)

    def check_emp_info(self):
        self.controller.dept_change.show()

    def clicked_back_btn(self):
        self.stackedWidget.setCurrentWidget(self.admin_home_page)

    # 현재 달에 해당하는 사용자 근태시간 그리기 위한 데이터 가져오기
    def set_graph_for_user(self, data):
        self.x_list, self.y_list = list(), list()
        # data = data[-10:]
        for i in data:
            date, start_time, end_time = i[1], i[2], i[7]
            if date != self.controller.dbconn.return_datetime('date'):  # 현재날짜는 제외
                hour_diff = 0
                if end_time != 'NULL':
                    time_difference = self.controller.dbconn.get_strptime(start_time, end_time)
                    hour_diff = time_difference.total_seconds() / 3600
                self.x_list.append(str(date[-2:]))
                self.y_list.append(int(hour_diff))

        # 그래프 그리기
        print('그래프 그리는 곳', self.x_list, self.y_list)
        if len(self.x_list) >=10:
            self.figure = self.create_plot_graph(self.x_list[-10:], self.y_list[-10:], '출근날짜', '출근시간')
        else:
            self.figure = self.create_plot_graph(self.x_list, self.y_list, '출근날짜', '출근시간')
        self.canvas = FigureCanvas(self.figure)
        self.verticalLayout_6.addWidget(self.canvas)


    # 선 그래프 그리기
    def create_plot_graph(self, x_list, y_list, x_lab='', y_lab='', layout=''):

        x_vals = np.linspace(0, len(x_list) - 1, 500)

        # 데이터 포인트의 수에 따라 보간 방식 결정
        if len(x_list) < 4:
            kind = 'linear'  # 또는 'quadratic'
        else:
            kind = 'cubic'

        y_interp = interp1d(np.arange(len(y_list)), y_list, kind=kind)
        y_vals = y_interp(x_vals)

        # 그래프 조건
        fig = Figure(figsize=(4, 1.6))
        fig.tight_layout()
        # fig.subplots_adjust(left=0.15, right=0.98, top=0.95, bottom=0.15)

        ax = fig.add_subplot(111)
        ax.plot(x_vals, y_vals, color='#3085FE')  # 부드럽게 그래프 그리기

        ax.set_ylim(0, max(y_vals) + 1)

        ax.set_xticks(np.arange(len(x_list)))  # x_list의 인덱스를 눈금 위치로 설정
        ax.set_xticklabels(x_list)  # x_list의 값들을 눈금 라벨로 설정

        # ax.set_xlabel(x_lab)
        # ax.set_ylabel(y_lab)
        ax.grid(False)

        return fig

    # 막대 그래프 그리기
    def create_bar_graph(self, x_list, y_list, x_lab='', y_lab='', title=''):

        fig, ax = plt.subplots(figsize=(4, 3))
        self.x_val, self.y_val = x_list, y_list
        ax.bar(x_list, y_list, color='#3085FE')
        ax.set_xlabel(x_lab)
        ax.set_ylabel(y_lab)
        ax.set_title(title)
        ax.set_xticks(x_list)  # x축의 눈금 위치 설정
        ax.set_xticklabels(x_list, rotation=45)  # x축의 눈금 라벨을 설정하고 45도로 회전
        ax.set_ylim(0, 100) # y축 크기 설정
        ax.grid(False)
        fig.tight_layout()
        # fig.subplots_adjust(left=0.15, right=0.98, top=0.95, bottom=0.15)

        return fig


    # 다중 막대 그래프 그리기
    def plot_multi_bar(self, data):
        # 팀 목록 추출
        depts = list(data.keys())

        # 모든 팀에서 사용된 월을 추출합니다.
        all_months = set()
        for dept in data:
            all_months.update(data[dept].keys())
        months = sorted(list(all_months))

        # 모든 팀에 대해 공통된 월 목록을 기반으로 데이터를 정리합니다.
        for dept in depts:
            for month in months:
                if month not in data[dept].keys():
                    data[dept][month] = 0  # 데이터가 없는 월은 0으로 처리합니다.

        x = np.arange(len(months))
        width = 1 / (len(depts) + 1)

        fig, ax = plt.subplots(figsize=(12, 7))
        colors = ["#3085FE", "#89B2FF", "#A9C6FF", "#B8D4FF", "#CBE2FF", "#D9EBFF"]
        for idx, dept in enumerate(depts):
            values = [data[dept][month] for month in months]
            ax.bar(x + idx * width, values, width, label=dept, color=colors[idx])

        ax.set_xticks(x + width * (len(depts) - 1) / 2)
        ax.set_xticklabels(months)
        ax.legend()

        fig.tight_layout()
        return fig

    def create_donut_chart(self, datas):
        labels, data = zip(*datas)
        colors = ["#3085FE", "#89B2FF", "#A9C6FF", "#B8D4FF", "#CBE2FF", "#D9EBFF"]

        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        # Helper function to display data values along with percentage
        def func(pct, allvals):
            absolute = int(pct / 100. * sum(allvals))
            return f"{pct:.1f}%\n({absolute:d})"

        # Create the pie chart using the ax object
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data), textprops=dict(color="w"),
                                          colors=colors)

        # Legend and other aesthetics
        ax.legend(wedges, labels, title="Labels", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=8, weight="bold")

        return fig

    def draw_team_donut_chart_for_admin(self):
        data = self.controller.dbconn.count_dept_emp()
        fig = self.create_donut_chart(data)
        canvas = FigureCanvas(fig)
        self.verticalLayout_22.addWidget(canvas)


    # 유저 달별 근태율 막대그래프 그리기
    def set_user_bar_graph(self, x_list, y_list, x_lab='', y_lab='', title='', layout=None):
        fig = self.create_bar_graph(x_list, y_list, x_lab, y_lab, title)
        canvas = FigureCanvas(fig)

        layout.addWidget(canvas)

    def set_dept_atd_per_bar_graph(self):
        data = self.controller.dbconn.return_team_atd_per()
        print(data)
        x, y = list(), list()
        for dept, per in data.items():
            x.append(dept)
            y.append(per)
        print(x, y)
        self.set_user_bar_graph(x_list=x, y_list=y, layout=self.verticalLayout_20)






    # 그래프 크게 띄우기 =====================
    def show_large_graph(self, event):
        new_fig = self.create_plot_graph(self.x_list, self.y_list, x_lab='출근날짜', y_lab='출근시간')
        new_canvas = FigureCanvas(new_fig)
        d = ShowGraph(new_canvas, '근무시간 그래프')
        d.exec_()

    def show_large_bar_graph(self, event):
        new_fig = self.create_bar_graph(self.x_val, self.y_val, x_lab='월별', y_lab='출근율', title='월별 출근울(%)')
        new_canvas = FigureCanvas(new_fig)
        d = ShowGraph(new_canvas, '월별 출근울(%)')
        d.exec_()

    # 관리자
    def show_large_admin_bar_graph(self, event):
        data = self.controller.dbconn.return_team_atd_per(type='graph')
        new_fig = self.plot_multi_bar(data)
        new_canvas = FigureCanvas(new_fig)
        d = ShowGraph(new_canvas, '팀별 근태율')
        d.exec_()

    def show_large_admin_donut_graph(self, event):
        data = self.controller.dbconn.count_dept_emp()
        fig = self.create_donut_chart(data)
        new_canvas = FigureCanvas(fig)
        d = ShowGraph(new_canvas, '팀원수')
        d.exec_()
