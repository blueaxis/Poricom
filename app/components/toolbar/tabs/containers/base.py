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

from PyQt5.QtCore import (QSize)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QWidget)

# TODO: config should be a constant
from utils.config import config

class BaseToolbarContainer(QWidget):
    """Widget that contains the toolbar functions

    Args:
        parent (QMainWindow, optional): Container parent. Set to main window.
    """
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        # Manually set parent since `addTab` method will reparent the widget
        self.mainWindow = parent
        self.buttonList: list[QPushButton] = []

    def addButton(self):
        """Adds a QPushButton object to `buttonList`

        Returns:
            QPushButton: Recently added QPushButton
        """
        self.buttonList.append(QPushButton(self))
        return self.buttonList[-1]

    def initializeButton(self, buttonName, buttonConfig):
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

        button = self.addButton()

        # Allows to programmatically interact with buttons
        button.setObjectName(buttonName)

        button.setIcon(icon)
        button.setIconSize(QSize(w, h))
        # TODO: Do not set fixed size
        button.setFixedSize(QSize(w*m, h*m))

        tooltip = f"<h3 style='margin-bottom: 4px;'>{buttonConfig['helpTitle']}\
            </h3><p style='margin-top: 0;'>{buttonConfig['helpMsg']}</p>"
        button.setToolTip(tooltip)
        button.setCheckable(buttonConfig["toggle"])

        if hasattr(self.mainWindow, buttonName):
            button.clicked.connect(
                getattr(self.mainWindow, buttonName))
        else:
            button.clicked.connect(
                getattr(self.mainWindow, 'poricomNoop'))
