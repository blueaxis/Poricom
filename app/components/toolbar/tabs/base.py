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

from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton, QWidget)

from utils.config import config

# TODO: Refactor this as a container
class BaseToolbarTab(QWidget):
    """Widget that contains the toolbar functions

    Args:
        parent (QWidget, optional): Toolbar tab parent. Set to main window.
        funcs (Any, optional): Toolbar function configuration. Defaults to {}.
        tracker (Any, optional): State tracker. Defaults to None.
        tabName (str, optional): Toolbar tab name. Defaults to "".
    """
    def __init__(self, parent: QMainWindow, funcs={}, tracker=None, tabName=""):
        # TODO: Add type to funcs and tracker
        # TODO: tracker and tabName might not be needed
        super(QWidget, self).__init__()

        # Manually set parent since `addTab` method will reparent the widget
        self.mainWindow = parent
        self.tracker = tracker
        self.tabName = tabName

        self.buttonList: list[QPushButton] = []
        self.setLayout(QHBoxLayout())
        # self.layout().setAlignment(Qt.AlignLeft)

        self.initializeButtons(funcs)

    def initializeButtons(self, funcs):

        for funcName, funcConfig in funcs.items():
            self.loadButtonConfig(funcName, funcConfig)
            # TODO: Alignment might be obsolete
            self.layout().addWidget(self.buttonList[-1],
                                  alignment=getattr(Qt, funcConfig["align"]))
        # self.layout.addStretch()
        # self.layout.addWidget(PageNavigator(self.mainWindow))

    def loadButtonConfig(self, buttonName, buttonConfig):
        # TODO: Base icon size on screen height instead of parent height
        w = self.mainWindow.frameGeometry().height(
        )*config["TBAR_ISIZE_REL"]*buttonConfig["iconW"]
        h = self.mainWindow.frameGeometry().height(
        )*config["TBAR_ISIZE_REL"]*buttonConfig["iconH"]
        m = config["TBAR_ISIZE_MARGIN"]

        icon = QIcon()
        path = config["TBAR_ICONS"] + buttonConfig["path"]
        if (exists(path)):
            icon = QIcon(path)
        else:
            icon = QIcon(config["TBAR_ICON_DEFAULT"])

        self.buttonList.append(QPushButton(self))

        # Allows to programmatically interact with buttons
        self.buttonList[-1].setObjectName(buttonName)

        self.buttonList[-1].setIcon(icon)
        self.buttonList[-1].setIconSize(QSize(w, h))
        # TODO: Do not set fixed size
        self.buttonList[-1].setFixedSize(QSize(w*m, h*m))

        tooltip = f"<h3 style='margin-bottom: 4px;'>{buttonConfig['helpTitle']}\
            </h3><p style='margin-top: 0;'>{buttonConfig['helpMsg']}</p>"
        self.buttonList[-1].setToolTip(tooltip)
        self.buttonList[-1].setCheckable(buttonConfig["toggle"])

        if hasattr(self.mainWindow, buttonName):
            self.buttonList[-1].clicked.connect(
                getattr(self.mainWindow, buttonName))
        else:
            self.buttonList[-1].clicked.connect(
                getattr(self.mainWindow, 'poricomNoop'))
