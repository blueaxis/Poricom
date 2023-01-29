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
from utils.constants import IMAGE_SCALING


class ImageScalingOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [IMAGE_SCALING])
        # TODO: Use constants here
        # TODO: Image scaling must be an enum not an int
        self.initializeProperties([("imageScaling", 0, int)])

    def changeImageScaling(self, i):
        self.imageScalingIndex = i

    def saveSettings(self, hasMessage=False):
        self.mainWindow.canvas.modifyViewImageMode(self.imageScalingIndex)
        return super().saveSettings(hasMessage)
