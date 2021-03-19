"""
Example 4 from QThreads and You

Author: Ben Sutton
Description: To be used with QThreads and You presentation linked here.
https://docs.google.com/presentation/d/1qgygq21cc5gx_A7Wm2egRztQ4e11USGpy7hVCFOk_Jw/edit?usp=sharing

"""

import inspect
import os
import sys
import time
from typing import List, Dict, Union, Optional

from PyQt5 import uic

from PyQt5.QtCore import Qt, QObject, QSize, pyqtSlot, pyqtSignal, QRegExp, QThread, QTimer
from PyQt5.QtGui import QFontDatabase, QMovie, QKeyEvent, QResizeEvent, QPixmap, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QWidget, QPushButton, QRadioButton, \
    QLineEdit, QProgressBar, QGroupBox, QComboBox, QCheckBox, QStackedWidget, QInputDialog, QGridLayout, QFormLayout, QSpacerItem


class ExampleWindow(QMainWindow):
    """
    Main GUI for Examples.
    """
    sig_custom = pyqtSignal()  # new signal to enable proper Affinity interaction

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(Qt.Window)

        self.setWindowTitle("Example")
        self.setMinimumSize(400, 150)

        print_tid("(pre-ui)")

        self.worker_thread = QThread(self)  # this time we use a separate QThread

        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)  # this time Worker's Thread Affinity is adjusted

        self.setup_ui()
        self.connect_signals_slots()

        print_tid("(post-ui)")

    def setup_ui(self):
        """
        Setup any UI components
        """
        lbl_title = QLabel("QThreading Example 4")
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

        self.worker_thread.started.connect(self.worker.run_it)  # links native QThread.started signal to new f() of Worker
        self.worker_thread.finished.connect(lambda: self.close())
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker.sig_worker_done.connect(self.worker_thread.quit)
        self.worker.sig_worker_done.connect(self.worker.deleteLater)

        self.sig_custom.connect(self.worker.mult_affinity)

    @pyqtSlot(bool)
    def on_slowstop_clicked(self, value: bool):
        print_tid()

        self.worker_thread.start()
        self.sig_custom.emit()  # emit the new signal to fire mult_affinity, notice how it queues BEHIND run_it

    @pyqtSlot()
    def closeEvent(self, *args, **kwargs):
        """
        Overloaded closeEvent
        :param args:
        :param kwargs:
        """
        print_tid()

    @pyqtSlot(QKeyEvent)
    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Escape:
            self.close()


class Worker(QObject):
    sig_worker_done = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot()  # a slot has now been declared to make mult_affinity work on the thread of it's affinity
    def mult_affinity(self):
        # Does not have a single Thread Affinity, danger Will Robinson
        print_tid()

    def run_it(self):
        print_tid("(starting)")
        time.sleep(5)

        print_tid("(finished)")
        self.sig_worker_done.emit()


def print_tid(comment=""):
    print(f"tid: {int(inspect.currentframe().f_back.f_locals['self'].thread().currentThreadId())}, from: {inspect.stack()[1][3]} {comment}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    test_window = ExampleWindow()

    test_window.show()

    sys.exit(app.exec())  # app.exec() starts event loop
