"""
Poricom Ribbon Components

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

from utils.config import config


class RibbonTab(QWidget):

    def __init__(self, parent=None, funcs=None, tracker=None, tabName=""):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker
        self.tabName = tabName

        self.buttonList = []
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)

        self.initButtons(funcs)

    def initButtons(self, funcs):

        for funcName, funcConfig in funcs.items():
            self.loadButtonConfig(funcName, funcConfig)
            self.layout.addWidget(self.buttonList[-1],
                                  alignment=getattr(Qt, funcConfig["align"]))
        self.layout.addStretch()
        self.layout.addWidget(PageNavigator(self.parent))

    def loadButtonConfig(self, buttonName, buttonConfig):

        w = self.parent.frameGeometry().height(
        )*config["TBAR_ISIZE_REL"]*buttonConfig["iconW"]
        h = self.parent.frameGeometry().height(
        )*config["TBAR_ISIZE_REL"]*buttonConfig["iconH"]
        m = config["TBAR_ISIZE_MARGIN"]

        icon = QIcon()
        path = config["TBAR_ICONS"] + buttonConfig["path"]
        if (exists(path)):
            icon = QIcon(path)
        else:
            icon = QIcon(config["TBAR_ICON_DEFAULT"])

        self.buttonList.append(QPushButton(self))
        self.buttonList[-1].setObjectName(buttonName)

        self.buttonList[-1].setIcon(icon)
        self.buttonList[-1].setIconSize(QSize(w, h))
        self.buttonList[-1].setFixedSize(QSize(w*m, h*m))

        tooltip = f"<h3 style='margin-bottom: 4px;'>{buttonConfig['helpTitle']}\
            </h3><p style='margin-top: 0;'>{buttonConfig['helpMsg']}</p>"
        self.buttonList[-1].setToolTip(tooltip)
        self.buttonList[-1].setCheckable(buttonConfig["toggle"])

        if hasattr(self.parent, buttonName):
            self.buttonList[-1].clicked.connect(
                getattr(self.parent, buttonName))
        else:
            self.buttonList[-1].clicked.connect(
                getattr(self.parent, 'poricomNoop'))


class PageNavigator(RibbonTab):

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker
        self.buttonList = []

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        for funcName, funcConfig in config["MODE_FUNCS"].items():
            self.loadButtonConfig(funcName, funcConfig)

        self.layout.addWidget(self.buttonList[0], 0, 0, 1, 1)
        self.layout.addWidget(self.buttonList[1], 1, 0, 1, 1)
        self.layout.addWidget(self.buttonList[2], 0, 1, 1, 2)
        self.layout.addWidget(self.buttonList[3], 1, 1, 1, 1)
        self.layout.addWidget(self.buttonList[4], 1, 2, 1, 1)


class Ribbon(QTabWidget):
    def __init__(self, parent=None, tracker=None):
        super(QTabWidget, self).__init__(parent)
        self.parent = parent
        self.tracker = tracker

        h = self.parent.frameGeometry().height(
        ) * config["TBAR_ISIZE_REL"] * config["RBN_HEIGHT"]
        self.setFixedHeight(h)

        for tabName, tools in config["TBAR_FUNCS"].items():
            self.addTab(RibbonTab(parent=self.parent, funcs=tools,
                        tracker=self.tracker, tabName=tabName), tabName)
