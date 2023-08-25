import sys
import cv2
import numpy as np
import os

from PyQt5.QtWidgets import QMessageBox, QLabel, QDialog, QApplication, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from create_dataset import start_capture

class YourPyQtClass(QDialog):  
    def __init__(self):
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()

        # Create components
        self.numimglabel = QLabel(self)
        self.image_label = QLabel(self)  # label to display the image
        capture_button = QPushButton("Capture Image", self)
        capture_button.clicked.connect(self.capimg)

        # Add components to layout
        layout.addWidget(self.image_label)
        layout.addWidget(self.numimglabel)
        layout.addWidget(capture_button)
        self.setLayout(layout)

        self.num_of_images = 0
        self.active_name = "soyeon"  # Adjust this if you have a different mechanism for active names

    @pyqtSlot()
    def capimg(self):
        self.numimglabel.setText("Captured Images = 0")

        # Capture image using OpenCV and display it
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.image_label.setPixmap(QPixmap.fromImage(q_img))
            cap.release()
        else:
            QMessageBox.warning(self, "Error", "Failed to capture the image.")

        # Other logic remains unchanged
        QMessageBox.information(self, "INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self, self.active_name)
        self.num_of_images = x
        self.numimglabel.setText("Number of images captured = {}".format(x))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YourPyQtClass()
    ex.show()
    sys.exit(app.exec_())
