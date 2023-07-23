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

from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget

from utils.constants import TRANSLATE_MODEL, TOGGLE_CHOICES, TRANSLATE_WINDOW_POSITION

from .base import BaseOptions


class TranslateOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(
            parent, [TOGGLE_CHOICES, TRANSLATE_MODEL, TRANSLATE_WINDOW_POSITION]
        )
        # TODO: Use constants here
        self.initializeProperties(
            [
                ("enableTranslate", "false", bool),
                ("translateModel", "ArgosTranslate", str),
                ("translateWindowPosition", "Right", str),
            ]
        )

        i = len(self.comboBoxList)
        self.apiLabel = QLabel("API Key")
        self.apiLineEdit = QLineEdit(self.mainWindow.state.translateApiKey, self)
        self.layout().addWidget(self.apiLabel, i, 0)
        self.layout().addWidget(self.apiLineEdit, i, 1)
        self.updateDisplay()

    def updateDisplay(self):
        translateModelName = self.translateModelComboBox.currentText().strip()
        if translateModelName == "ArgosTranslate":
            self.apiLabel.hide()
            self.apiLineEdit.hide()
        elif translateModelName == "ChatGPT" or translateModelName == "DeepL":
            self.apiLabel.show()
            self.apiLineEdit.show()
        else:
            self.apiLabel.hide()
            self.apiLineEdit.hide()

    def changeEnableTranslate(self, i):
        self.enableTranslateIndex = i
        self.enableTranslate = True if i else False

    def changeTranslateModel(self, i):
        self.translateModelIndex = i
        try:
            self.updateDisplay()
        # Handle case where extra widgets are still undefined
        except AttributeError as e:
            print(e)

    def changeTranslateWindowPosition(self, i):
        self.translateWindowPosition = TRANSLATE_WINDOW_POSITION[i]

    def saveSettings(self, hasMessage=True):
        translateModelName = self.translateModelComboBox.currentText().strip()
        translateApiKey = self.apiLineEdit.text().strip()
        self.mainWindow.state.setTranslateModelName(translateModelName)
        self.mainWindow.state.setTranslateApiKey(translateApiKey)
        self.mainWindow.state.setTranslateWindowPosition(self.translateWindowPosition)
        self.mainWindow.setProperty(
            "enableTranslate", "true" if self.enableTranslate else "enableTranslate"
        )
        return super().saveSettings(hasMessage)
