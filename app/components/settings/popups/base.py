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

from stringcase import titlecase, capitalcase
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QGridLayout, QLabel, QWidget

from ..base import BaseSettings


class BaseOptions(BaseSettings):
    """
    Allows saving/selecting options
    """

    def __init__(self, parent: QWidget, optionLists: list[list[str]] = []):
        super().__init__(parent)
        self.mainWindow = parent
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
        """Set the combo box index based on the option name

        Args:
            option (str): Option name in camelcase
            index (int, optional): Combo box index. Defaults to 0.
        """
        optionIndex = self.settings.value(f"{option}Index", index, int)
        comboBox = self.getProperty(f"{option}ComboBox")
        comboBox.setCurrentIndex(optionIndex)
        self.addProperty(f"{option}Index", optionIndex, int)

    def initializeProperties(self, props: list[tuple[str, Any, Callable]]):
        """Initialize property values and names

        Args:
            props (list[tuple[str, Any, Callable]]): List of props. \
            Each prop must have the following format: (name, default, type).
            It is recommended that the name is in camelcase.

        Note:
            Child classes must implement change{PropName} method
        """
        for i, p in enumerate(props):
            # Property
            prop, propDefault, propType = p
            self.addProperty(prop, propDefault, propType)

            # Label
            label = self.labelList[i]
            label.setText(f"{titlecase(prop)}: ")
            self.setProperty(f"{prop}Label", label)

            # Combo Box
            comboBox = self.comboBoxList[i]
            self.setProperty(f"{prop}ComboBox", comboBox)

            # Child classes must implement change{PropName} method
            comboBox.currentIndexChanged.connect(
                self.getProperty(f"change{capitalcase(prop)}")
            )
            self.setOptionIndex(prop)
