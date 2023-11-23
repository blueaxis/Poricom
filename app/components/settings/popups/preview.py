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

from PyQt5.QtWidgets import QWidget

from .base import BaseOptions
from utils.constants import FONT_SIZE, FONT_STYLE, TOGGLE_CHOICES
from utils.scripts import editStylesheet


class PreviewOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [FONT_STYLE, FONT_SIZE, TOGGLE_CHOICES])
        self.initializeProperties(
            [
                ("fontStyle", "  font-family: 'Helvetica';\n", str),
                ("fontSize", "  font-size: 16pt;\n", str),
                ("persistText", "true", bool),
            ]
        )
        self.setOptionIndex("fontSize", 2)
        self.setOptionIndex("persistText", 1)

    def changeFontStyle(self, i):
        self.fontStyleIndex = i
        selectedFontStyle = self.fontStyleComboBox.currentText().strip()
        replacementText = f"  estilo-fuente: '{selectedFontStyle}';\n"
        self.fontStyle = replacementText

    def changeFontSize(self, i):
        self.fontSizeIndex = i
        selectedFontSize = int(self.fontSizeComboBox.currentText().strip())
        replacementText = f"  tamaño-fuente: {selectedFontSize}pt;\n"
        self.fontSize = replacementText

    def changePersistText(self, i):
        self.persistTextIndex = i
        self.persistText = True if i else False

    def saveSettings(self, hasMessage=False):
        editStylesheet(41, self.fontStyle)
        editStylesheet(42, self.fontSize)
        self.mainWindow.canvas.setProperty(
            "persistText", "true" if self.persistText else "false"
        )
        return super().saveSettings(hasMessage)
