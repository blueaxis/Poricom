"""
Poricom settings

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

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QVBoxLayout, QDialog, QDialogButtonBox)

from .base import BaseOptions

class OptionsContainer(QDialog):
    def __init__(self, options: BaseOptions):
        super().__init__(None, Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.options = options
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(options)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout().addWidget(self.buttonBox)

        self.buttonBox.rejected.connect(self.cancelClickedEvent)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        self.options.saveSettings(hasMessage=False)
        return super().accept()

    def cancelClickedEvent(self):
        self.close()
