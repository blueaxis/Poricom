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

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget

from components.popups import BasePopup
from utils.constants import SETTINGS_FILE_DEFAULT


class BaseSettings(QWidget):
    """Base settings widget to allow save/load/reset of settings

    Args:
        parent (QWidget): Parent widget. Set to SettingsMenu object.
        file (str): Path to configuration file. Must be in ini format. Defaults to SETTINGS_FILE_DEFAULT.
        prefix (str, optional): Text added to the saved property. Defaults to "".
    """

    def __init__(
        self, parent: QWidget, file: str = SETTINGS_FILE_DEFAULT, prefix: str = ""
    ):
        super().__init__(parent)
        self.settings = QSettings(file, QSettings.IniFormat)

        # Settings widgets may sometimes share the same configuration file.
        # Set the prefix to a unique value to avoid this.
        self._prefix = prefix

        self.setDefaults({})
        self.setTypes({})

    def setDefaults(self, defaults: dict[str, Any]):
        """Set the default dictionary

        `self._defaults` contains the default values for ALL properties.
        Any property that is saved/loaded from settings should have a default.
        Otherwise, the property will not be saved/loaded.
        """
        self._defaults = defaults

    def addDefaults(self, defaults: dict[str, Any]):
        """
        Extends the defaults dictionary, if it exists
        """
        try:
            self.setDefaults({**self._defaults, **defaults})
        except AttributeError:
            self.setDefaults(defaults)

    def setTypes(self, types: dict[str, Callable]):
        """Set the types dictionary

        By default, if the value is a non-QVariant, it is read as a str.
        Use `self._types` to set the correct property type.
        """
        self._types = types

    def addTypes(self, types: dict[str, Callable]):
        """
        Extends the types dictionary, if it exists
        """
        try:
            self.setTypes({**self._types, **types})
        except AttributeError:
            self.setTypes(types)

    def getProperty(self, prop: str):
        return getattr(self, prop)

    def setProperty(self, prop: str, value: Any):
        try:
            t = self._types[prop]
            if t == bool:
                v = value if type(value) == bool else value.lower() == "true"
                return setattr(self, prop, v)
            return setattr(self, prop, t(value))
        except KeyError:
            return setattr(self, prop, value)

    def addProperty(self, prop: str, value: Any, t: Callable = str):
        self._defaults[prop] = value
        self._types[prop] = t
        self.setProperty(prop, value)

    def removeProperty(self, prop: str):
        del self._defaults[prop]
        del self._types[prop]

    def saveSettings(self, hasMessage=True):
        for propName, _ in self._defaults.items():
            self.settings.setValue(
                f"{self._prefix}{propName}", self.getProperty(propName)
            )
        if hasMessage:
            BasePopup("Save Settings", "Configuration has been saved.").exec()

    def loadSettings(self, settings: dict[str, Any] = {}):
        if not settings:
            settings = self._defaults
        for propName, propDefault in settings.items():
            prop = self.settings.value(f"{self._prefix}{propName}", propDefault)
            self.setProperty(propName, prop)

    def confirmResetSettings(self):
        confirm = BasePopup(
            "Reset Settings",
            "Are you sure? This will delete the current configuration.",
            BasePopup.Ok | BasePopup.Cancelar,
        )
        response = confirm.exec()
        if response == BasePopup.Ok:
            self.resetSettings()

    def resetSettings(self):
        try:
            self.settings.clear()
        except Exception:
            pass
        self.loadSettings()
