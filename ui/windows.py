import os
import shutil
import sys

from qtpy import QtWidgets, QtGui, QtCore
from qtpy.QtCore import Qt
from functools import partial
import string
import qtawesome as qta
from ui import widgets

ITEM_UI_KEYS = [
    "filename",
    "tags",
    "rating",
    "playcount",
    "skipcount",
    "duration",
    "date",
    "lastplayed",
]

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("WebmCol")

        # contents
        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)

        self.search_bar = widgets.SearchBarWidget(self.main_widget)
        self.main_layout.addWidget(self.search_bar)

        self.collection_table = widgets.CollectionTableWidget(self.main_widget)
        self.main_layout.addWidget(self.collection_table)

        self.setCentralWidget(self.main_widget)


        # menu bar
        self.menu_bar = self.menuBar()
        view_menu = self.menu_bar.addMenu("&View")
        self.header_options = [True for _ in range(len(ITEM_UI_KEYS))]  # TODO: or load from saved config

        # header options
        for i, item_key in enumerate(ITEM_UI_KEYS):
            header_option_action = QtWidgets.QAction("&" + str(item_key).title(), self)
            header_option_action.setCheckable(True)
            header_option_action.setChecked(self.header_options[i])
            header_option_action.triggered.connect(partial(self._header_toggled, i))
            view_menu.addAction(header_option_action)

        # library stuff
        self.library_menu = self.menu_bar.addMenu("&Library")
        new_library_action = QtWidgets.QAction("Add &New", self)
        self.library_menu.addAction(new_library_action)


        # dragging and dropping files
        self.setAcceptDrops(True)

    def _header_toggled(self, n):
        self.header_options[n] = not self.header_options[n]  # toggle
        print("{}".format(n))
        print(self.header_options)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent):
        for url in event.mimeData().urls():
            print(url.toLocalFile())
