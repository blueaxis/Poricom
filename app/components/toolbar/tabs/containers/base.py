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
from PyQt5.QtWidgets import (QMainWindow, QPushButton)

from components.misc import ScreenAwareWidget
from utils.constants import TOOLBAR_ICON_DEFAULT, TOOLBAR_ICON_SIZE, TOOLBAR_ICONS
from utils.types import ButtonConfig

class BaseToolbarContainer(ScreenAwareWidget):
    """Widget that contains the toolbar functions

    Args:
        parent (QMainWindow): Container parent. Set to main window.
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

    def initializeButton(self, name: str, config: ButtonConfig):
        button = self.addButton()

        # Allows to programmatically interact with buttons
        button.setObjectName(name)

        # Set button icon and size
        path = TOOLBAR_ICONS + config["path"]
        if (exists(path)):
            icon = QIcon(path)
        else:
            icon = QIcon(TOOLBAR_ICON_DEFAULT)
        button.setIcon(icon)
        w = self.primaryScreenHeight()*TOOLBAR_ICON_SIZE*config["iconWidth"]
        h = self.primaryScreenHeight()*TOOLBAR_ICON_SIZE*config["iconHeight"]
        button.setIconSize(QSize(w, h))

        tooltip = f"\
            <h3 style='margin-bottom: 4px;'>{config['title']}</h3>\
            <p style='margin-top: 0;'>{config['message']}</p>\
        "
        button.setToolTip(tooltip)

        button.setCheckable(config["toggle"])

        # Connect button to main window function
        try:
            button.clicked.connect(
                getattr(self.mainWindow, name))
        except AttributeError:
            try:
                button.clicked.connect(
                    getattr(self.mainWindow.mainView, name))
            except AttributeError:
                button.clicked.connect(
                    getattr(self.mainWindow, 'poricomNoop'))
