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

from typing import Any, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QGridLayout, QLabel, QWidget)
from stringcase import titlecase, capitalcase

from ..base import BaseSettings


class BaseOptions(BaseSettings):
    def __init__(self, parent: QWidget, optionLists:list[list[str]]=[]):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.comboBoxList: list[QComboBox] = []
        self.labelList: list[QLabel] = []

        for i in range(len(optionLists)):
            optionList = optionLists[i]

            self.comboBoxList.append(QComboBox())
            self.comboBoxList[i].addItems(optionList)
            self.layout().addWidget(self.comboBoxList[i], i, 1)
            self.labelList.append(QLabel(""))
            self.layout().addWidget(self.labelList[i], i, 0)

    def setOptionIndex(self, option: str, index: int = 0):
        optionIndex = self.settings.value(f"{option}Index", index, int)
        comboBox = self.getProperty(f"{option}ComboBox")
        comboBox.setCurrentIndex(optionIndex)
        self.addProperty(f"{option}Index", optionIndex, int)

    def addOptionProperties(self, props: list[tuple[str, Any, Callable]]):
        for i, p in enumerate(props):
            # Property
            prop, propDefault, propType = p
            self.addProperty(prop, propDefault, propType)

            # Label
            self.labelList[i].setText(f"{titlecase(prop)}: ")
            
            # Combo Box
            comboBox = self.comboBoxList[i]
            self.setProperty(f"{prop}ComboBox", comboBox)
            comboBox.currentIndexChanged.connect(self.getProperty(f"change{capitalcase(prop)}"))
            self.setOptionIndex(prop)