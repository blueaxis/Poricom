"""
Poricom Toolbar

Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from os.path import exists

from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtWidgets import (
    QGridLayout, QHBoxLayout, QWidget, QTabWidget, QPushButton)

from .tabs import BaseToolbarTab, NavigateToolbarContainer
from utils.config import config


class BaseToolbar(QTabWidget):
    def __init__(self, parent=None, tracker=None):
        super(QTabWidget, self).__init__(parent)
        self.parent = parent
        self.tracker = tracker

        h = self.parent.frameGeometry().height(
        ) * config["TBAR_ISIZE_REL"] * config["RBN_HEIGHT"]
        self.setFixedHeight(h)

        for tabName, tools in config["TBAR_FUNCS"].items():
            tab = BaseToolbarTab(parent=self.parent, funcs=tools,
                        tracker=self.tracker, tabName=tabName)
            tab.layout().addStretch()
            tab.layout().addWidget(
                NavigateToolbarContainer(self.parent, self.tracker))
            self.addTab(tab, tabName)
