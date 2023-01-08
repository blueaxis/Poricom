"""
Poricom Views

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

from time import sleep

from PyQt5.QtCore import (Qt, QRect, QRectF, QSize, QThreadPool)
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView, QMainWindow)

from ..ocr import BaseOCRView
from Popups import MessagePopup
from components.services import BaseWorker

# TODO: This should be the other way around. OCRView should inherit from ImageView
class BaseImageView(BaseOCRView):
    """
    Base image view to allow view/zoom/pan functions 
    """

    def __init__(self, parent: QMainWindow, tracker=None):
        super().__init__(parent, tracker)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self._viewImageMode = parent.config["VIEW_IMAGE_MODE"]
        self._splitViewMode = parent.config["SPLIT_VIEW_MODE"]
        self._zoomPanMode = False
        self.currentScale = 0

        self._scrollAtMin = 0
        self._scrollAtMax = 0
        self._trackPadAtMin = 0
        self._trackPadAtMax = 0
        self._scrollSuppressed = False

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(self.tracker.pixImage.scaledToWidth(
            self.viewport().geometry().width(), Qt.SmoothTransformation))

    def viewImage(self):
        # self.verticalScrollBar().setSliderPosition(0)
        self.currentScale = 0
        w = self.viewport().geometry().width()
        h = self.viewport().geometry().height()
        if self._viewImageMode == 0:
            self.pixmap.setPixmap(
                self.tracker.pixImage.scaledToWidth(w, Qt.SmoothTransformation))
        elif self._viewImageMode == 1:
            self.pixmap.setPixmap(
                self.tracker.pixImage.scaledToHeight(h, Qt.SmoothTransformation))
        elif self._viewImageMode == 2:
            self.pixmap.setPixmap(self.tracker.pixImage.scaled(
                w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    # TODO: Cloe settings component might be useful
    def setViewImageMode(self, mode):
        self._viewImageMode = mode
        self.parent.config["VIEW_IMAGE_MODE"] = mode
        self.parent.config["SELECTED_INDEX"]['imageScaling'] = mode
        self.viewImage()

    def splitViewMode(self):
        return self._splitViewMode

    def toggleSplitView(self):
        self._splitViewMode = not self._splitViewMode
        self.parent.config["SPLIT_VIEW_MODE"] = self._splitViewMode

    def zoomView(self, isZoomIn):
        if isZoomIn and self.currentScale < 8:
            factor = 1.25
            self.currentScale += 1
            self.scale(factor, factor)
        elif not isZoomIn and self.currentScale > -8:
            factor = 0.8
            self.currentScale -= 1
            self.scale(factor, factor)

    def toggleZoomPanMode(self):
        self._zoomPanMode = not self._zoomPanMode

    def resizeEvent(self, event):
        self.viewImage()
        super().resizeEvent(event)

    def wheelEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        zoomMode = pressedKey == Qt.ControlModifier or self._zoomPanMode

        # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # TODO: Rewrite individual event handlers as separate functions
        if zoomMode:
            if event.angleDelta().y() > 0:
                isZoomIn = True
            elif event.angleDelta().y() < 0:
                isZoomIn = False
            self.zoomView(isZoomIn)

        if self._scrollSuppressed:
            return

        if not zoomMode:

            mouseScrollLimit = 3
            trackpadScrollLimit = 36
            wheelDelta = 120

            def suppressScroll():
                self._scrollSuppressed = True
                worker = BaseWorker(sleep, 0.3)
                worker.signals.finished.connect(
                    lambda: setattr(self, "_scrollSuppressed", False))
                QThreadPool.globalInstance().start(worker)

            if (event.angleDelta().y() < 0 and
                    self.verticalScrollBar().value() == self.verticalScrollBar().maximum()):
                if (event.angleDelta().y() > -wheelDelta):
                    if (self._trackPadAtMax == trackpadScrollLimit):
                        self.parent.loadNextImage()
                        self._trackPadAtMax = 0
                        suppressScroll()
                        return
                    else:
                        self._trackPadAtMax += 1
                elif (event.angleDelta().y() <= -wheelDelta):
                    if (self._scrollAtMax == mouseScrollLimit):
                        self.parent.loadNextImage()
                        self._scrollAtMax = 0
                        suppressScroll()
                        return
                    else:
                        self._scrollAtMax += 1

            if (event.angleDelta().y() > 0 and
                    self.verticalScrollBar().value() == self.verticalScrollBar().minimum()):
                if (event.angleDelta().y() < wheelDelta):
                    if (self._trackPadAtMin == trackpadScrollLimit):
                        self.parent.loadPrevImage()
                        self._trackPadAtMin = 0
                        suppressScroll()
                        return
                    else:
                        self._trackPadAtMin += 1
                elif (event.angleDelta().y() >= wheelDelta):
                    if (self._scrollAtMin == mouseScrollLimit):
                        self.parent.loadPrevImage()
                        self._scrollAtMin = 0
                        suppressScroll()
                        return
                    else:
                        self._scrollAtMin += 1
            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        panMode = pressedKey == Qt.ControlModifier or self._zoomPanMode

        if panMode:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.RubberBandDrag)

        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.currentScale = 1
        self.viewImage(self.currentScale)
        super().mouseDoubleClickEvent(event)

    # TODO: Keyboard shortcuts should be in another class
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.parent.loadPrevImage()
            return
        if event.key() == Qt.Key_Right:
            self.parent.loadNextImage()
            return
        if event.key() == Qt.Key_Minus:
            self.zoomView(isZoomIn=False)
            return
        if event.key() == Qt.Key_Plus:
            self.zoomView(isZoomIn=True)
            return
        super().keyPressEvent(event)
