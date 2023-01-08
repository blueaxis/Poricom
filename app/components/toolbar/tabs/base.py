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

from PyQt5.QtWidgets import (QHBoxLayout, QMainWindow)

from .containers import BaseToolbarContainer
from utils.types import ButtonConfigDict

class BaseToolbarTab(BaseToolbarContainer):
    """Tab widget to arrange toolbar tab containers

    Args:
        parent (QMainWindow): Toolbar tab parent. Set to main window.
        funcs (ButtonConfigDict, optional): Toolbar function configuration. Defaults to {}.
    """
    def __init__(self, parent: QMainWindow, funcs: ButtonConfigDict={}):
        super().__init__(parent)

        self.initializeButtons(funcs)

    def initializeButtons(self, funcs: ButtonConfigDict):
        self.setLayout(QHBoxLayout())
        for name, config in funcs.items():
            self.initializeButton(name, config)
            self.layout().addWidget(self.buttonList[-1])
