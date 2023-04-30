"""
Poricom Workspace View Component

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

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QSplitter

from .ocr import OCRView
from components.explorers import ImageExplorer
from components.popups import BasePopup
from components.settings import BaseSettings, ImageScalingOptions, OptionsContainer
from services import BaseWorker, State
from utils.constants import EXPLORER_ROOT_DEFAULT, MAIN_VIEW_DEFAULTS, MAIN_VIEW_RATIO
from utils.scripts import mangaFileToImageDir


class WorkspaceView(QSplitter, BaseSettings):
    """
    Main view of the program. Includes the explorer and the view.
    """

    def __init__(self, parent: QMainWindow, state: State):
        super().__init__(parent)
        self.mainWindow = parent
        self.state = state

        self.setDefaults(MAIN_VIEW_DEFAULTS)
        self.loadSettings()

        self.canvas = OCRView(self, self.state)
        self.explorer = ImageExplorer(self, self.explorerPath)
        self.addWidget(self.explorer)
        self.addWidget(self.canvas)
        self.setChildrenCollapsible(False)
        for i, s in enumerate(MAIN_VIEW_RATIO):
            self.setStretchFactor(i, s)

    def resizeEvent(self, event):
        self.explorer.setMinimumWidth(0.1 * self.width())
        self.canvas.setMinimumWidth(0.7 * self.width())
        return super().resizeEvent(event)

    # ------------------------------------ Explorer ------------------------------------- #

    def openDir(self):
        filepath = self.explorer.getDirectory(self.explorerPath)

        if filepath:
            self.explorer.setDirectory(filepath)
            self.explorerPath = filepath
        elif filepath == None:
            BasePopup(
                "No images found",
                "Please select a directory with images.",
            ).exec()

    def openManga(self):
        filename = self.explorer.getDirectory(self.explorerPath, True)

        if filename:
            self.explorerPath = EXPLORER_ROOT_DEFAULT

            worker = BaseWorker(mangaFileToImageDir, filename)
            worker.signals.result.connect(self.explorer.setDirectory)
            QThreadPool.globalInstance().start(worker)

    def hideExplorer(self):
        self.explorer.setVisible(not self.explorer.isVisible())

    # -------------------------------------- View --------------------------------------- #

    def viewImageFromExplorer(self, filename, filenext):
        if not self.canvas.splitViewMode:
            self.state.baseImage = filename
        if self.canvas.splitViewMode:
            self.state.baseImage = (filename, filenext)
        if not self.state.baseImage.isValid():
            return False
        self.canvas.resetTransform()
        self.canvas.currentScale = 1
        self.canvas.verticalScrollBar().setSliderPosition(0)
        self.canvas.viewImage()
        return True

    def toggleSplitView(self):
        self.canvas.toggleSplitView()
        if self.canvas.splitViewMode:
            self.canvas.modifyViewImageMode(2)
            index = self.explorer.currentIndex()
            self.explorer.currentChanged(index, index)
        elif not self.canvas.splitViewMode:
            index = self.explorer.currentIndex()
            self.explorer.currentChanged(index, index)

    def modifyImageScaling(self):
        OptionsContainer(ImageScalingOptions(self)).exec()

    # -------------------------------------- Zoom --------------------------------------- #

    def toggleMouseMode(self):
        self.canvas.toggleZoomPanMode()

    def zoomIn(self):
        self.canvas.zoomView(True)

    def zoomOut(self):
        self.canvas.zoomView(False)

    # ----------------------------------- Navigation ------------------------------------ #

    def loadPrevImage(self):
        index = self.explorer.indexAbove(self.explorer.currentIndex())
        if self.canvas.splitViewMode:
            tempIndex = self.explorer.indexAbove(index)
            if tempIndex.isValid():
                index = tempIndex
        if not index.isValid():
            return
        self.explorer.setCurrentIndex(index)

    def loadNextImage(self):
        index = self.explorer.indexBelow(self.explorer.currentIndex())
        if self.canvas.splitViewMode:
            tempIndex = self.explorer.indexBelow(index)
            if tempIndex.isValid():
                index = tempIndex
        if not index.isValid():
            return
        self.explorer.setCurrentIndex(index)

    def loadImageAtIndex(self):
        rowCount = self.explorer.model().rowCount(self.explorer.rootIndex())
        i, _ = QInputDialog.getInt(
            self,
            "Jump to",
            f"Enter page number: (max is {rowCount})",
            value=-1,
            min=1,
            max=rowCount,
            flags=Qt.CustomizeWindowHint | Qt.WindowTitleHint,
        )
        if i == -1:
            return

        index = self.explorer.model().index(i - 1, 0, self.explorer.rootIndex())
        self.explorer.setCurrentIndex(index)
