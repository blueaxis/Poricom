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

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QGridLayout, QVBoxLayout, QWidget, QLabel, QCheckBox,
                             QLineEdit, QComboBox, QDialog, QDialogButtonBox, QMessageBox)

from utils.constants import LANGUAGE, ORIENTATION

from .base import BaseOptions

class TesseractOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [LANGUAGE, ORIENTATION])
        # TODO: Use constants here
        self.addOptionProperties([("language", "jpn", str), ("orientation", "_vert", str)])

    def changeLanguage(self, i):
        self.languageIndex = i
        selectedLanguage = self.languageComboBox.currentText().strip()
        if selectedLanguage == "Japanese":
            self.language = "jpn"
        if selectedLanguage == "Korean":
            self.language = "kor"
        if selectedLanguage == "Chinese SIM":
            self.language = "chi_sim"
        if selectedLanguage == "Chinese TRA":
            self.language = "chi_tra"
        if selectedLanguage == "English":
            self.language = "eng"

    def changeOrientation(self, i):
        self.orientationIndex = i
        selectedOrientation = self.orientationComboBox.currentText().strip()
        if selectedOrientation == "Vertical":
            self.orientation = "_vert"
        if selectedOrientation == "Horizontal":
            self.orientation = ""
