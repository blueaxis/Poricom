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

from PyQt5.QtWidgets import (QGridLayout, QMainWindow)

from .base import BaseToolbarContainer
from utils.constants import NAVIGATION_FUNCTIONS

class NavigateToolbarContainer(BaseToolbarContainer):
    """Widget that contains the toolbar navigation functions

    Args:
        parent (QWidget, optional): Container parent. Set to main window.
    """

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        self.initializeButtons()

    def initializeButtons(self):
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        for name, config in NAVIGATION_FUNCTIONS.items():
            self.initializeButton(name, config)

        self.layout().addWidget(self.buttonList[0], 0, 0, 1, 1)
        self.layout().addWidget(self.buttonList[1], 1, 0, 1, 1)
        self.layout().addWidget(self.buttonList[2], 0, 1, 1, 2)
        self.layout().addWidget(self.buttonList[3], 1, 1, 1, 1)
        self.layout().addWidget(self.buttonList[4], 1, 2, 1, 1)
