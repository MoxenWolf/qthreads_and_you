"""
Example 1 from QThreads and You

Author: Ben Sutton
Description: To be used with QThreads and You presentation linked here.
https://docs.google.com/presentation/d/1qgygq21cc5gx_A7Wm2egRztQ4e11USGpy7hVCFOk_Jw/edit?usp=sharing

"""

import os
import sys
import time
from typing import List, Dict, Union, Optional

from PyQt5 import uic

from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, QRegExp, QThread, QTimer
from PyQt5.QtGui import QFontDatabase, QMovie, QKeyEvent, QResizeEvent, QPixmap, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QWidget, QPushButton, QRadioButton, \
    QLineEdit, QProgressBar, QGroupBox, QComboBox, QCheckBox, QStackedWidget, QInputDialog, QGridLayout, QFormLayout, QSpacerItem


class ExampleWindow(QMainWindow):
    """
    Main GUI for Examples.
    """

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(Qt.Window)

        self.setWindowTitle("Example")
        self.setMinimumSize(400, 150)

        print(f"{self.thread().currentThreadId()}: Thread ID (pre-ui)")
        print(f"{int(self.thread().currentThreadId())}")

        self.setup_ui()
        self.connect_signals_slots()

        print(f"{self.thread().currentThreadId()}: Thread ID (post-ui)")
        print(f"{int(self.thread().currentThreadId())}")

    def setup_ui(self):
        """
        Setup any UI components
        """
        lbl_title = QLabel("QThreading Example 1")
        self.btn_slowstop = QPushButton("Push to Slowly Close")

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QFormLayout())

        self.centralWidget().layout().addWidget(lbl_title)
        self.centralWidget().layout().addWidget(QLabel(" "))
        self.centralWidget().layout().addWidget(self.btn_slowstop)

    def connect_signals_slots(self):
        """
        Connect any signals / slots
        """
        self.btn_slowstop.clicked.connect(self.on_slowstop_clicked)

    @pyqtSlot(bool, name="on_slowstop_clicked")
    def on_slowstop_clicked(self, value: bool):
        print(f"{self.thread().currentThreadId()}: Thread ID (on_slowstop_clicked)")
        print(f"{int(self.thread().currentThreadId())}")

        for x in range(10):
            print(f"inside at position {x}")
            time.sleep(1.0)  # mimicking large processing load

        self.close()

    @pyqtSlot()
    def closeEvent(self, *args, **kwargs):
        """
        Overloaded closeEvent
        :param args:
        :param kwargs:
        """
        print("...closing")

    @pyqtSlot(QKeyEvent)
    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    test_window = ExampleWindow()

    test_window.show()

    sys.exit(app.exec())  # app.exec() starts event loop
