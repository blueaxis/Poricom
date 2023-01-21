"""
Poricom Settings

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

from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget

from .base import BaseOptions
from components.popups import BasePopup
from utils.constants import MODIFIER


class ShortcutOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [MODIFIER])
        self.initializeProperties([("modifier", "Alt", str)])
        self.setOptionIndex("modifier", 2)
        self.addDefaults(
            {"captureExternalKey": "Q", "captureExternalShortcut": "Alt+Q"}
        )
        self.loadSettings()

        self.keyLineEdit = QLineEdit(self.captureExternalKey)
        self.layout().addWidget(self.keyLineEdit, 1, 1)
        self.layout().addWidget(QLabel("Key: "), 1, 0)

    def raiseKeyInvalidError(self, message: str):
        BasePopup("Invalid Key", message).exec()

    def changeModifier(self, i):
        self.modifierIndex = i
        self.modifier = self.modifierComboBox.currentText().strip() + "+"
        if self.modifier == "No Modifier+":
            self.modifier = ""

    def changeShortcut(self):
        self.captureExternalShortcut = self.modifier + self.captureExternalKey

    def saveSettings(self, hasMessage=False):
        if not self.keyLineEdit.text().isalnum():
            self.raiseKeyInvalidError("Please select an alphanumeric key.")
            return
        if len(self.keyLineEdit.text()) != 1:
            self.raiseKeyInvalidError("Please select exactly one key.")
            return
        self.captureExternalKey = self.keyLineEdit.text()

        self.changeShortcut()

        super().saveSettings(hasMessage)

        BasePopup("Shortcut Remapped", "Close the app to apply changes.").exec()
