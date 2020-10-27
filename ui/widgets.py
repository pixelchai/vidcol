import os
import shutil
import sys

from qtpy import QtWidgets, QtGui, QtCore
from qtpy.QtCore import Qt
from functools import partial
import string
import qtawesome as qta

class CollectionTableWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.table_headers = ["Filename", "Tags", "Rating"]

        self.table = QtWidgets.QTableWidget(self)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)  # makes the text in the headers left-aligned
        self.table.verticalHeader().hide()  # remove vertical header
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # enforce that when a cell is clicked, the entire row is selected
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # do not allow the cells' text to be edited
        self.table.horizontalHeader().setHighlightSections(False)  # the headers no longer become bold when cells are selected
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # when right click is clicked (or any other equivalent action), fire the 'customContextMenuRequested' signal
        self.layout.addWidget(self.table)

        # fake data:
        self._clear_table()
        self.table.setRowCount(1)
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem("Bob.webm"))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem("fat cat sat mat"))
        tmp_combo = QtWidgets.QComboBox()
        tmp_combo.addItems(["0", "1", "2"])
        self.table.setCellWidget(0, 2, tmp_combo)

    def _set_table_headers(self):
        num_headers = len(self.table_headers)  # get the number of headers

        self.table.setColumnCount(num_headers)  # set the column count
        self.table.setHorizontalHeaderLabels(self.table_headers)  # add the header labels

        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)  # make the first column 'stretch' to take up all remaining space

        # make all subsequent columns resize to fit their contents
        for i in range(1, num_headers):
            self.table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def _clear_table(self):
        self.table.clear()  # completely clear the table.
        # Note: this also removes the header, columns, etc
        self._set_table_headers()  # table headers must always be set again after table is cleared

class SearchBarWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # search box
        self.search_box = QtWidgets.QLineEdit(self)

        self.layout.addWidget(self.search_box, 1)

        # Clear button
        self.btn_clear = QtWidgets.QToolButton(self)
        self.btn_clear.setContentsMargins(0, 0, 0, 0)
        self.btn_clear.setIcon(qta.icon('fa.times'))
        self.btn_clear.clicked.connect(self._btn_clear_clicked)
        self.layout.addWidget(self.btn_clear, 0, Qt.AlignRight)

        # Search button
        self.btn_search = QtWidgets.QToolButton(self)
        self.btn_search.setContentsMargins(0, 0, 0, 0)
        self.btn_search.setIcon(qta.icon('fa.search'))
        self.layout.addWidget(self.btn_search, 0, Qt.AlignRight)

        self.setLayout(self.layout)

    def _btn_clear_clicked(self):
        # clear search box's text and trigger search button
        self.search_box.clear()
        self.btn_search.click()