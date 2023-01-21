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

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QCheckBox

from components.popups import BasePopup
from utils.constants import SETTINGS_FILE_DEFAULT


class CheckboxPopup(BasePopup):
    """Popup message with a checkbox

    Args:
        prop (str): Name of the boolean property to be saved.
        checkboxMessage (str, optional): Checkbox label.
        Defaults to "Don't show this dialog again".
    """

    def __init__(
        self,
        prop: str,
        title: str,
        message: str,
        buttons: BasePopup.StandardButtons = BasePopup.Ok,
        checkboxMessage="Don't show this dialog again",
    ):
        super().__init__(title, message, buttons)

        self.setCheckBox(QCheckBox(checkboxMessage, self))

        self.prop = prop
        self.accepted.connect(self.saveSettings)

    def saveSettings(self):
        settings = QSettings(SETTINGS_FILE_DEFAULT, QSettings.IniFormat)
        settings.setValue(self.prop, not self.checkBox().isChecked())
