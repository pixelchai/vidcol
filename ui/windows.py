import os
import shutil
import sys

from qtpy import QtWidgets, QtGui, QtCore
from qtpy.QtCore import Qt
from functools import partial
import string
import qtawesome as qta
from util import logger

from library import LibraryManager, Library
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
        self.library_manager = LibraryManager()
        self.library = self.library_manager.get_last_library()


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


        # menu bar
        self.menu_bar = self.menuBar()
        view_menu = self.menu_bar.addMenu("&View")
        self.header_options = [True for _ in range(len(ITEM_UI_KEYS))]  # TODO: or load from saved config

        # header options
        for i, item_key in enumerate(ITEM_UI_KEYS):
            header_option_action = QtWidgets.QAction("&" + str(item_key).title(), self)
            header_option_action.setCheckable(True)
            header_option_action.setChecked(self.header_options[i])
            header_option_action.triggered.connect(partial(self._toggle_header, i))
            view_menu.addAction(header_option_action)

        # library stuff
        self.library_menu = self.menu_bar.addMenu("&Library")
        self.library_actions = []

        self.modify_library_action = QtWidgets.QAction("&Modify", self)
        self.modify_library_action.triggered.connect(self._modify_library)
        self._load_library_menu()

        # dragging and dropping files
        self.setAcceptDrops(True)

    def _load_library_menu(self):
        self.library_menu.clear()

        for library_name in self.library_manager.names:
            library_action = QtWidgets.QAction("&" + str(library_name), self)
            library_action.setCheckable(True)
            library_action.setChecked(library_name == self.library.name)
            library_action.triggered.connect(partial(self._switch_to_library, library_name))
            self.library_menu.addAction(library_action)
            self.library_actions.append(library_action)

        self.library_menu.addSeparator()
        self.library_menu.addAction(self.modify_library_action)

    def _toggle_header(self, i):
        self.header_options[i] = not self.header_options[i]  # toggle
        logger.debug("Toggled header: {}".format(ITEM_UI_KEYS[i]))

    def _switch_to_library(self, name):
        self.library.close()  # may be unnecessary since library_manager may handle for us
        self.library = self.library_manager.get_library(name)

        for i, library_action in enumerate(self.library_actions):
            library_action.setChecked(self.library_manager.names[i] == name)
        logger.debug("Library switched to: {}".format(name))

        # if library requires password, enter it
        # todo: implement

    def _modify_library(self):
        def on_window_closed():
            logger.debug("Library mod window closed")
            self._load_library_menu()  # refresh library menu

        library_mod_window = LibraryModificationWindow(self, self.library_manager)
        library_mod_window.close_signal.connect(on_window_closed)
        library_mod_window.show()

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent):
        for url in event.mimeData().urls():
            print(url.toLocalFile())

    def closeEvent(self, event):
        self.library.close()
        self.windowTitle()
        self.library_manager.close()

class CloseableWindow(QtWidgets.QMainWindow):
    close_signal = QtCore.Signal()  # https://stackoverflow.com/a/37640029/5013267

    def closeEvent(self, event):
        self.close_signal.emit()

class LibraryModificationWindow(CloseableWindow):
    def __init__(self, parent, library_manager: "LibraryManager"):
        super().__init__(parent)
        self.library_manager = library_manager
        self.setWindowTitle(parent.windowTitle() + " - Library Modification")

        self.setFixedWidth(400)
        self.setFixedHeight(200)

        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)

        # list widget
        self.list_widget = QtWidgets.QListWidget(self.main_widget)
        self.list_widget.itemSelectionChanged.connect(self._list_selection_changed)
        self.main_layout.addWidget(self.list_widget)
        self._load_list()

        # button bar
        self.button_bar = widgets.ModificationButtonsBar(self.main_widget)
        self._update_buttons()
        self.main_layout.addWidget(self.button_bar)

        self.setCentralWidget(self.main_widget)

    def _load_list(self):
        self.list_widget.clear()
        for library_name in self.library_manager.names:
            self.list_widget.addItem(library_name)

    def _update_buttons(self):
        enabled = len(self.list_widget.selectedItems()) > 0
        self.button_bar.btn_minus.setEnabled(enabled)
        self.button_bar.btn_edit.setEnabled(enabled)

    def _list_selection_changed(self):
        self._update_buttons()

if __name__ == '__main__':
    # # for debug only:
    # app = QtWidgets.QApplication([])
    # window = LibraryModificationWindow()
    #
    # window.show()
    # app.exec_()
    pass
