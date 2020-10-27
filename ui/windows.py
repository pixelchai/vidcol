import os
import shutil
import sys

from qtpy import QtWidgets, QtGui, QtCore
from qtpy.QtCore import Qt
from functools import partial
import string
import qtawesome as qta
from ui import widgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("VidCol")

        # contents
        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)

        self.search_bar = widgets.SearchBarWidget(self.main_widget)
        self.main_layout.addWidget(self.search_bar)

        self.collection_table = widgets.CollectionTableWidget(self.main_widget)
        self.main_layout.addWidget(self.collection_table)

        self.setCentralWidget(self.main_widget)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    main_window = MainWindow()
    main_window.show()
    app.exec_()