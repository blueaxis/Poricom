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

from PyQt5.QtWidgets import (
    QGridLayout, QPushButton)

from .base import BaseToolbarTab
from utils.config import config

class NavigateToolbarContainer(BaseToolbarTab):
    """Widget that contains the toolbar navigation functions

    Args:
        parent (QWidget, optional): Toolbar tab parent. Set to main window. Defaults to None.
        tracker (Any, optional): State tracker. Defaults to None.
    """

    def __init__(self, parent=None, tracker=None):
        super().__init__(parent)
        self.parent = parent
        self.tracker = tracker
        self.buttonList: QPushButton = []

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        for funcName, funcConfig in config["MODE_FUNCS"].items():
            self.loadButtonConfig(funcName, funcConfig)

        self.layout.addWidget(self.buttonList[0], 0, 0, 1, 1)
        self.layout.addWidget(self.buttonList[1], 1, 0, 1, 1)
        self.layout.addWidget(self.buttonList[2], 0, 1, 1, 2)
        self.layout.addWidget(self.buttonList[3], 1, 1, 1, 1)
        self.layout.addWidget(self.buttonList[4], 1, 2, 1, 1)
