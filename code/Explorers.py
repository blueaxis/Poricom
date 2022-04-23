"""
Poricom Explorer Components

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

from PyQt5.QtCore import (Qt, QDir)
from PyQt5.QtWidgets import (QTreeView, QFileSystemModel)

from utils.config import config


class ImageExplorer(QTreeView):
    layoutCheck = False

    def __init__(self, parent=None, tracker=None):
        super(QTreeView, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.model = QFileSystemModel()
        # self.model.setFilter(QDir.Files)
        self.model.setNameFilterDisables(False)
        self.model.setNameFilters(config["IMAGE_EXTENSIONS"])
        self.setModel(self.model)

        for i in range(1, 4):
            self.hideColumn(i)
        self.setIndentation(0)

        self.setDirectory(tracker.filepath)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def currentChanged(self, current, previous):
        if not current.isValid():
            current = self.model.index(0, 0, self.rootIndex())
        filename = self.model.fileInfo(current).absoluteFilePath()
        nextIndex = self.indexBelow(current)
        filenext = self.model.fileInfo(nextIndex).absoluteFilePath()
        self.parent.viewImageFromExplorer(filename, filenext)
        QTreeView.currentChanged(self, current, previous)

    def setTopIndex(self):
        topIndex = self.model.index(0, 0, self.rootIndex())
        if topIndex.isValid():
            self.setCurrentIndex(topIndex)
            if self.layoutCheck:
                self.model.layoutChanged.disconnect(self.setTopIndex)
                self.layoutCheck = False
        else:
            if not self.layoutCheck:
                self.model.layoutChanged.connect(self.setTopIndex)
                self.layoutCheck = True

    def setDirectory(self, path):
        self.setRootIndex(self.model.setRootPath(path))
        self.setTopIndex()
