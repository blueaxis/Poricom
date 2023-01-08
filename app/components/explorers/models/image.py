"""
Poricom Explorers
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

from PyQt5.QtCore import (QModelIndex)
from PyQt5.QtWidgets import (QFileSystemModel)

from utils.constants import IMAGE_EXTENSIONS

class ImageModel(QFileSystemModel):
    """
    Image model based on the native file system
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setNameFilterDisables(False)
        self.setNameFilters(IMAGE_EXTENSIONS)

    def getTopIndex(self, parentIndex: QModelIndex):
        """Get the index of the top most file in the view

        Args:
            parentIndex (QModelIndex): Root index of the parent view

        Returns:
            int: Index of the top most file
        """
        item = self.index(0, 0, parentIndex)
        if self.fileInfo(item).isFile():
            return 0

        r = self.rowCount(parentIndex) // 2
        while True:
            item = self.index(r, 0, parentIndex)
            if not item.isValid():
                break
            if self.fileInfo(item).isFile():
                r //= 2
            elif not self.fileInfo(item).isFile():
                r += 1
                item = self.index(r, 0, parentIndex)
                if self.fileInfo(item).isFile():
                    break
        return r
