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

from PyQt5.QtWidgets import (QMainWindow, QSizePolicy, QTabWidget)

from .tabs import BaseToolbarTab, NavigateToolbarContainer
from utils.constants import TOOLBAR_FUNCTIONS

class BaseToolbar(QTabWidget):
    """
    Toolbar widget

    Args:
        parent (QMainWindow): Toolbar parent. Set to main window.
    Notes:
        Parent must be passed to children to call main window functions.
    """
    def __init__(self, parent: QMainWindow):
        super(QTabWidget, self).__init__(parent)
        self.parent = parent

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        for tabName, funcs in TOOLBAR_FUNCTIONS.items():
            tab = BaseToolbarTab(parent=self.parent, funcs=funcs)
            tab.layout().addStretch()
            tab.layout().addWidget(
                NavigateToolbarContainer(self.parent))
            self.addTab(tab, tabName.upper())
