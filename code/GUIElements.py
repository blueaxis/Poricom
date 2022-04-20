"""
Poricom
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

from os.path import exists

from PyQt5.QtGui import (QIcon, QTransform)
from PyQt5.QtCore import (Qt, QDir, QSize, QRectF, QTimer, pyqtSlot)
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout,
                            QApplication, QTreeView, QFileSystemModel,
                            QWidget, QTabWidget, QPushButton,
                            QGraphicsView, QGraphicsScene, QLabel)

import image_io as io_
from utils.config import config, editConfig

# TODO: Decorate slots using pyqtSlot

class ImageNavigator(QTreeView):
    layoutCheck = False
    def __init__(self, parent=None, tracker=None):
        super(QTreeView, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.model = QFileSystemModel()
        self.model.setFilter(QDir.Files)
        self.model.setNameFilterDisables(False)
        self.model.setNameFilters(config["IMAGE_EXTENSIONS"])
        self.setModel(self.model)

        for i in range(1,4):
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
        self.parent.view_image_from_explorer(filename, filenext)
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

class BaseCanvas(QGraphicsView):

    def __init__(self, parent=None, tracker=None):
        super(QGraphicsView, self).__init__(parent)
        self.parent = parent
        self.tracker = tracker

        self.timer_ = QTimer()
        self.timer_.setInterval(300)
        self.timer_.setSingleShot(True)
        self.timer_.timeout.connect(self.rubberBandStopped)

        self.canvasText = QLabel("", self, Qt.WindowStaysOnTopHint)
        self.canvasText.hide()
        self.canvasText.setObjectName("canvasText")

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(self.tracker.p_image.scaledToWidth(
            self.viewport().geometry().width(), Qt.SmoothTransformation))
        
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mouseMoveEvent(self, event):
        # TODO: There is rare bug where if the rubber band is moved too 
        # fast and is released near the point where the mouse is pressed,
        # PIL.UnidentifiedImageError occurs because the size of the image
        # is 0 bytes.
        rubberBandVisible = not self.rubberBandRect().isNull()
        if (event.buttons() & Qt.LeftButton) and rubberBandVisible:
            self.timer_.start()
        QGraphicsView.mouseMoveEvent(self, event)
    
    def mouseReleaseEvent(self, event):
        log_path = self.tracker.filepath + "/log.txt"
        log_to_file = self.tracker.write_mode
        text = self.canvasText.text()
        io_.logText(text, mode=log_to_file, path=log_path)
        self.canvasText.hide()
        super().mouseReleaseEvent(event)

    @pyqtSlot()
    def rubberBandStopped(self):

        # use threading either here or on image_io
        if (self.canvasText.isHidden()):
            self.canvasText.show()

        lang = self.tracker.language + self.tracker.orientation
        pixbox = self.grab(self.rubberBandRect())
        text = io_.pixboxToText(pixbox, lang, 
            self.tracker.ocr_model)

        self.canvasText.setText(text)
        self.canvasText.adjustSize()

class FullScreen(BaseCanvas):

    def __init__(self, parent=None, tracker=None):
        super().__init__(parent, tracker)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def takeScreenshot(self):
        screen = QApplication.primaryScreen()
        s = screen.size()
        self.pixmap.setPixmap(
            screen.grabWindow(0).scaled(s.width(), s.height()))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def mouseReleaseEvent(self, event):
        BaseCanvas.mouseReleaseEvent(self, event)
        self.parent.close()

class OCRCanvas(BaseCanvas):

    def __init__(self, parent=None, tracker=None):
        super().__init__(parent, tracker)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self._viewImageMode = config["VIEW_IMAGE_MODE"]
        self._splitViewMode = config["SPLIT_VIEW_MODE"]
        self._zoomPanMode = False
        self.currentScale = 1
        self._scrollAtMin = 0
        self._scrollAtMax = 0

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(self.tracker.p_image.scaledToWidth(
            self.viewport().geometry().width(), Qt.SmoothTransformation))

    def viewImage(self):
        self.verticalScrollBar().setSliderPosition(0)
        if self._viewImageMode == 0:
            self.pixmap.setPixmap(self.tracker.p_image.scaledToWidth(
                self.viewport().geometry().width(), Qt.SmoothTransformation))
        elif self._viewImageMode == 1:
            self.pixmap.setPixmap(self.tracker.p_image.scaledToHeight(
                self.viewport().geometry().height(), Qt.SmoothTransformation))
        elif self._viewImageMode == 2:
            self.pixmap.setPixmap(self.tracker.p_image.scaled(
                self.viewport().geometry().width(), self.viewport().geometry().height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def setViewImageMode(self, mode):
        self._viewImageMode = mode
        editConfig("VIEW_IMAGE_MODE", mode)
        self.parent.config["VIEW_IMAGE_MODE"] = mode
        self.parent.config["SELECTED_INDEX"]['image_scaling'] = mode
        self.viewImage()

    def splitViewMode(self):
        return self._splitViewMode

    def toggleSplitView(self):
        self._splitViewMode = not self._splitViewMode
        editConfig("SPLIT_VIEW_MODE", self._splitViewMode)
        self.parent.config["SPLIT_VIEW_MODE"] = self._splitViewMode

    def zoomView(self, isZoomIn, usingButton=False):
        factor = 1.1
        if usingButton:
            factor = 1.4

        if isZoomIn and self.currentScale < 15:
            self.scale(factor, factor)
            self.currentScale *= factor
        elif not isZoomIn and self.currentScale > 0.35:
            self.scale(1/factor, 1/factor)
            self.currentScale /= factor

    def toggleZoomPanMode(self):
        self._zoomPanMode = not self._zoomPanMode

    def resizeEvent(self, event):
        self.viewImage()
        QGraphicsView.resizeEvent(self, event)

    def wheelEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        zoomMode = pressedKey == Qt.ControlModifier or self._zoomPanMode

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if zoomMode:
            if event.angleDelta().y() > 0:
                isZoomIn = True
            elif event.angleDelta().y() < 0:
                isZoomIn = False
            self.zoomView(isZoomIn)

        if not zoomMode:
            if (event.angleDelta().y() < 0 and
                self.verticalScrollBar().value() == self.verticalScrollBar().maximum()):
                if (self._scrollAtMax == 3):
                    self.parent.load_next_image()
                    self._scrollAtMax = 0
                    return
                else:
                    self._scrollAtMax += 1

            if (event.angleDelta().y() > 0 and
                self.verticalScrollBar().value() == self.verticalScrollBar().minimum()):
                if (self._scrollAtMin == 3):
                    self.parent.load_prev_image()
                    self._scrollAtMin = 0
                    return
                else:
                    self._scrollAtMin += 1
            QGraphicsView.wheelEvent(self, event)

    def mouseMoveEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        panMode = pressedKey == Qt.ControlModifier or self._zoomPanMode

        if panMode:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.RubberBandDrag)

        BaseCanvas.mouseMoveEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        self.setTransform(QTransform())
        self.currentScale = 1
        QGraphicsView.mouseDoubleClickEvent(self, event)
