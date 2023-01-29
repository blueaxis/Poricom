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

from os import listdir, path as ospath
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QTreeView

from .models import ImageModel
from utils.constants import EXPLORER_ROOT_DEFAULT, IMAGE_EXTENSIONS

if TYPE_CHECKING:
    from components.views import WorkspaceView


class ImageExplorer(QTreeView):
    """View to allow exploring images

    Args:
        parent (WorkspaceView): Image explorer parent. Set to workspace view.
        initialDir (str, optional): Initial directory. Defaults to EXPLORER_ROOT_DEFAULT.
    """

    def __init__(
        self, parent: "WorkspaceView", initialDir: str = EXPLORER_ROOT_DEFAULT
    ):
        super().__init__(parent)
        self.setModel(ImageModel())

        for i in range(1, 4):
            self.hideColumn(i)
        self.setIndentation(0)

        self.layoutCheck = False
        if not ospath.exists(initialDir):
            initialDir = EXPLORER_ROOT_DEFAULT
        self.setDirectory(initialDir)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setDirectory(self, path: str):
        self.setRootIndex(self.model().setRootPath(path))
        self.setTopIndex()

    def getDirectory(self, startPath: str, isManga=False):
        if isManga:
            filename, _ = QFileDialog.getOpenFileName(
                self.parent(),
                "Open Manga File",
                startPath,
                "Manga (*.cbz *.cbr *.zip *.rar *.pdf)",
            )
            return filename
        filepath = QFileDialog.getExistingDirectory(
            self.parent(), "Open Directory", startPath
        )
        if not filepath:
            return filepath
        for file in listdir(filepath):
            try:
                _, extension = file.split(".")
                if "*." + extension in IMAGE_EXTENSIONS:
                    return filepath
            except ValueError:
                continue
        return None

    def currentChanged(self, current, previous):
        if not current.isValid():
            current = self.model().index(self.getTopIndex(), 0, self.rootIndex())
        filename = self.model().fileInfo(current).absoluteFilePath()
        nextIndex = self.indexBelow(current)
        filenext = self.model().fileInfo(nextIndex).absoluteFilePath()
        self.parent().viewImageFromExplorer(filename, filenext)
        super().currentChanged(current, previous)

    def getTopIndex(self):
        return self.model().getTopIndex(self.rootIndex())

    def setTopIndex(self):
        topIndex = self.model().index(self.getTopIndex(), 0, self.rootIndex())
        if topIndex.isValid():
            self.setCurrentIndex(topIndex)
            if self.layoutCheck:
                self.model().layoutChanged.disconnect(self.setTopIndex)
                self.layoutCheck = False
        else:
            if not self.layoutCheck:
                self.model().layoutChanged.connect(self.setTopIndex)
                self.layoutCheck = True
