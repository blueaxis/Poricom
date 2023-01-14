"""
Poricom Main Window Component

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

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QInputDialog, QMainWindow, QSplitter)

from .ocr import BaseOCRView
from components.explorers import ImageExplorer
from utils.config import config
from utils.constants import MAIN_VIEW_RATIO

class MainView(QSplitter):

    def __init__(self, parent: QMainWindow, tracker=None):
        super().__init__(parent)
        self.tracker = tracker
        self.config = config

        self.canvas = BaseOCRView(self, self.tracker)
        self.explorer = ImageExplorer(self, self.tracker.filepath)

        self.addWidget(self.explorer)
        self.addWidget(self.canvas)
        self.setChildrenCollapsible(False)
        for i, s in enumerate(MAIN_VIEW_RATIO):
            self.setStretchFactor(i, s)

    def viewImageFromExplorer(self, filename, filenext):
        if not self.canvas.splitViewMode:
            self.tracker.pixImage = filename
        if self.canvas.splitViewMode:
            self.tracker.pixImage = (filename, filenext)
        if not self.tracker.pixImage.isValid():
            return False
        self.canvas.resetTransform()
        self.canvas.currentScale = 1
        self.canvas.verticalScrollBar().setSliderPosition(0)
        self.canvas.viewImage()
        # self.canvas.setFocus()
        return True

    def loadPrevImage(self):
        index = self.explorer.indexAbove(self.explorer.currentIndex())
        if self.canvas.splitViewMode:
            tempIndex = self.explorer.indexAbove(index)
            if tempIndex.isValid():
                index = tempIndex
        if (not index.isValid()):
            return
        self.explorer.setCurrentIndex(index)

    def loadNextImage(self):
        index = self.explorer.indexBelow(self.explorer.currentIndex())
        if self.canvas.splitViewMode:
            tempIndex = self.explorer.indexBelow(index)
            if tempIndex.isValid():
                index = tempIndex
        if (not index.isValid()):
            return
        self.explorer.setCurrentIndex(index)

    def loadImageAtIndex(self):
        rowCount = self.explorer.model().rowCount(self.explorer.rootIndex())
        i, _ = QInputDialog.getInt(
            self,
            'Jump to',
            f'Enter page number: (max is {rowCount})',
            value=-1,
            min=1,
            max=rowCount,
            flags=Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        if (i == -1):
            return

        index = self.explorer.model().index(i-1, 0, self.explorer.rootIndex())
        self.explorer.setCurrentIndex(index)

    def zoomIn(self):
        self.canvas.zoomView(True)

    def zoomOut(self):
        self.canvas.zoomView(False)

    def resizeEvent(self, event):
        self.explorer.setMinimumWidth(0.1*self.width())
        self.canvas.setMinimumWidth(0.6*self.width())
        return super().resizeEvent(event)
