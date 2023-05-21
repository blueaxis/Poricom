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

from utils.constants import LANGUAGE, OCR_MODEL, ORIENTATION, TOGGLE_CHOICES

from .base import BaseOptions


class ModelOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [OCR_MODEL, TOGGLE_CHOICES, LANGUAGE, ORIENTATION])
        # TODO: Use constants here
        self.initializeProperties(
            [
                ("ocrModel", "MangaOCR", str),
                ("useOcrOffline", "false", bool),
                ("language", "jpn", str),
                ("orientation", "_vert", str),
            ]
        )
        self.updateDisplay()

    def updateDisplay(self):
        ocrModelName = self.ocrModelComboBox.currentText().strip()
        if ocrModelName == "MangaOCR":
            self.languageLabel.hide()
            self.languageComboBox.hide()
            self.orientationLabel.hide()
            self.orientationComboBox.hide()
        elif ocrModelName == "Tesseract":
            self.languageLabel.show()
            self.languageComboBox.show()
            self.orientationLabel.show()
            self.orientationComboBox.show()
        else:
            self.languageLabel.show()
            self.languageComboBox.show()
            self.orientationLabel.hide()
            self.orientationComboBox.hide()

    def changeOcrModel(self, i):
        self.ocrModelIndex = i
        try:
            self.updateDisplay()
        # Handle case where extra widgets are still undefined
        except AttributeError as e:
            print(e)

    def changeUseOcrOffline(self, i):
        self.useOcrOfflineIndex = i
        self.useOcrOffline = True if i else False

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

    def saveSettings(self, hasMessage=True):
        ocrModelName = self.ocrModelComboBox.currentText().strip()
        self.mainWindow.state.setOCRModelName(ocrModelName)
        self.mainWindow.setProperty(
            "useOcrOffline", "true" if self.useOcrOffline else "useOcrOffline"
        )
        return super().saveSettings(hasMessage)
