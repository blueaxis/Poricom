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
from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt, QRect, QRectF, QSize, QThreadPool
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView

from components.services import BaseWorker
from components.settings import BaseSettings
from utils.constants import IMAGE_VIEW_DEFAULT, IMAGE_VIEW_TYPES

if TYPE_CHECKING:
    from ..workspace import WorkspaceView


class BaseImageView(QGraphicsView, BaseSettings):
    """
    Base image view to allow view/zoom/pan functions
    """

    def __init__(self, parent: "WorkspaceView", tracker=None):
        super().__init__(parent)
        self.tracker = tracker

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.currentScale = 0

        self._scrollAtMin = 0
        self._scrollAtMax = 0
        self._trackPadAtMin = 0
        self._trackPadAtMax = 0
        self._scrollSuppressed = False

        self.addDefaults(IMAGE_VIEW_DEFAULT)
        self.addTypes(IMAGE_VIEW_TYPES)
        self.loadSettings()

        self.initializePixmapItem()

    # ------------------------------------ Settings ------------------------------------- #

    def setViewImageMode(self, mode: int):
        # TODO: This should be an enum not an int
        self.setProperty("viewImageMode", mode)
        self.saveSettings(hasMessage=False)
        self.viewImage()

    def toggleSplitView(self):
        self.setProperty("splitViewMode", "false" if self.splitViewMode else "true")
        self.saveSettings(hasMessage=False)

    def toggleZoomPanMode(self):
        self.setProperty("zoomPanMode", "false" if self.zoomPanMode else "true")
        self.saveSettings(hasMessage=False)

    # -------------------------------------- View --------------------------------------- #

    def initializePixmapItem(self):
        self.setScene(QGraphicsScene())
        self.pixmap = self.scene().addPixmap(
            self.tracker.pixImage.scaledToWidth(
                self.viewport().geometry().width(), Qt.SmoothTransformation
            )
        )

    def viewImage(self):
        # self.verticalScrollBar().setSliderPosition(0)
        self.currentScale = 0
        w = self.viewport().geometry().width()
        h = self.viewport().geometry().height()
        if self.viewImageMode == 0:
            self.pixmap.setPixmap(
                self.tracker.pixImage.scaledToWidth(w, Qt.SmoothTransformation)
            )
        elif self.viewImageMode == 1:
            self.pixmap.setPixmap(
                self.tracker.pixImage.scaledToHeight(h, Qt.SmoothTransformation)
            )
        elif self.viewImageMode == 2:
            self.pixmap.setPixmap(
                self.tracker.pixImage.scaled(
                    w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        self.scene().setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def zoomView(self, isZoomIn):
        if isZoomIn and self.currentScale < 8:
            factor = 1.25
            self.currentScale += 1
            self.scale(factor, factor)
        elif not isZoomIn and self.currentScale > -8:
            factor = 0.8
            self.currentScale -= 1
            self.scale(factor, factor)

    def resizeEvent(self, event):
        self.viewImage()
        super().resizeEvent(event)

    def wheelEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        zoomMode = pressedKey == Qt.ControlModifier or self.zoomPanMode

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
                    lambda: setattr(self, "_scrollSuppressed", False)
                )
                QThreadPool.globalInstance().start(worker)

            if (
                event.angleDelta().y() < 0
                and self.verticalScrollBar().value()
                == self.verticalScrollBar().maximum()
            ):
                if event.angleDelta().y() > -wheelDelta:
                    if self._trackPadAtMax == trackpadScrollLimit:
                        self.parent().loadNextImage()
                        self._trackPadAtMax = 0
                        suppressScroll()
                        return
                    else:
                        self._trackPadAtMax += 1
                elif event.angleDelta().y() <= -wheelDelta:
                    if self._scrollAtMax == mouseScrollLimit:
                        self.parent().loadNextImage()
                        self._scrollAtMax = 0
                        suppressScroll()
                        return
                    else:
                        self._scrollAtMax += 1

            if (
                event.angleDelta().y() > 0
                and self.verticalScrollBar().value()
                == self.verticalScrollBar().minimum()
            ):
                if event.angleDelta().y() < wheelDelta:
                    if self._trackPadAtMin == trackpadScrollLimit:
                        self.parent().loadPrevImage()
                        self._trackPadAtMin = 0
                        suppressScroll()
                        return
                    else:
                        self._trackPadAtMin += 1
                elif event.angleDelta().y() >= wheelDelta:
                    if self._scrollAtMin == mouseScrollLimit:
                        self.parent().loadPrevImage()
                        self._scrollAtMin = 0
                        suppressScroll()
                        return
                    else:
                        self._scrollAtMin += 1
            super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        panMode = pressedKey == Qt.ControlModifier or self.zoomPanMode

        if panMode:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.RubberBandDrag)

        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.currentScale = 1
        self.viewImage(self.currentScale)
        super().mouseDoubleClickEvent(event)

    # ------------------------------------ Shortcut ------------------------------------- #

    # TODO: Keyboard shortcuts should be in another class
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.parent().loadPrevImage()
            return
        if event.key() == Qt.Key_Right:
            self.parent().loadNextImage()
            return
        if event.key() == Qt.Key_Minus:
            self.zoomView(isZoomIn=False)
            return
        if event.key() == Qt.Key_Plus:
            self.zoomView(isZoomIn=True)
            return
        super().keyPressEvent(event)
