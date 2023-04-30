"""
Poricom Popups

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

from PyQt5.QtWidgets import QWidget

from utils.constants import OCR_MODEL, TOGGLE_CHOICES

from .base import BaseOptions


class ModelOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [OCR_MODEL, TOGGLE_CHOICES])
        # TODO: Use constants here
        self.initializeProperties(
            [("ocrModel", "MangaOCR", str), ("useOcrOffline", "false", bool)]
        )

    def changeOcrModel(self, i):
        self.ocrModelIndex = i

    def changeUseOcrOffline(self, i):
        self.useOcrOfflineIndex = i
        self.useOcrOffline = True if i else False

    def saveSettings(self, hasMessage=True):
        ocrModelName = self.ocrModelComboBox.currentText()
        self.mainWindow.state.setOCRModelName(ocrModelName)
        self.mainWindow.setProperty(
            "useOcrOffline", "true" if self.useOcrOffline else "useOcrOffline"
        )
        return super().saveSettings(hasMessage)
