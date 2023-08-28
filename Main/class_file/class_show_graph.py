from Main.UI.ShowGraph import Ui_ShowGraph
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from Main.class_file.class_font import Font


class ShowGraph(QDialog, Ui_ShowGraph):
    def __init__(self, canvas, graph_title):
        super().__init__()
        self.setupUi(self)

        self.clear_layout(self.verticalLayout)
        self.label.setFont(Font.title(2))
        self.pushButton.setFont(Font.text(3, weight='bold'))

        # 투명하게 함
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 캔버스 추가
        self.verticalLayout.addWidget(canvas)
        self.label.setText(graph_title)
        self.pushButton.clicked.connect(self.close)

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
