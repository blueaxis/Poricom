"""
Poricom View Components

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

from PyQt5.QtGui import (QTransform)
from PyQt5.QtCore import (Qt, QRectF, QTimer, pyqtSlot)
from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QLabel)

from utils.image_io import logText, pixboxToText


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
        self.pixmap = self.scene.addPixmap(self.tracker.pixImage.scaledToWidth(
            self.viewport().geometry().width(), Qt.SmoothTransformation))

        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mouseMoveEvent(self, event):
        rubberBandVisible = not self.rubberBandRect().isNull()
        if (event.buttons() & Qt.LeftButton) and rubberBandVisible:
            self.timer_.start()
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        logPath = self.tracker.filepath + "/log.txt"
        logToFile = self.tracker.writeMode
        text = self.canvasText.text()
        logText(text, mode=logToFile, path=logPath)
        self.canvasText.hide()
        super().mouseReleaseEvent(event)

    @pyqtSlot()
    def rubberBandStopped(self):

        # use threading either here or on image_io
        if (self.canvasText.isHidden()):
            self.canvasText.show()

        lang = self.tracker.language + self.tracker.orientation
        pixbox = self.grab(self.rubberBandRect())
        text = pixboxToText(pixbox, lang,
                            self.tracker.ocrModel)

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
        self.pixmap.setPixmap(screen.grabWindow(
            0).scaled(s.width(), s.height()))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def mouseReleaseEvent(self, event):
        BaseCanvas.mouseReleaseEvent(self, event)
        self.parent.close()


class OCRCanvas(BaseCanvas):

    def __init__(self, parent=None, tracker=None):
        super().__init__(parent, tracker)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self._viewImageMode = parent.config["VIEW_IMAGE_MODE"]
        self._splitViewMode = parent.config["SPLIT_VIEW_MODE"]
        self._zoomPanMode = False
        self.currentScale = 1
        self._scrollAtMin = 0
        self._scrollAtMax = 0

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(self.tracker.pixImage.scaledToWidth(
            self.viewport().geometry().width(), Qt.SmoothTransformation))

    def viewImage(self):
        self.verticalScrollBar().setSliderPosition(0)
        if self._viewImageMode == 0:
            self.pixmap.setPixmap(self.tracker.pixImage.scaledToWidth(
                self.viewport().geometry().width(), Qt.SmoothTransformation))
        elif self._viewImageMode == 1:
            self.pixmap.setPixmap(self.tracker.pixImage.scaledToHeight(
                self.viewport().geometry().height(), Qt.SmoothTransformation))
        elif self._viewImageMode == 2:
            self.pixmap.setPixmap(self.tracker.pixImage.scaled(self.viewport().geometry().width(
            ), self.viewport().geometry().height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

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
                    self.parent.loadNextImage()
                    self._scrollAtMax = 0
                    return
                else:
                    self._scrollAtMax += 1

            if (event.angleDelta().y() > 0 and
                    self.verticalScrollBar().value() == self.verticalScrollBar().minimum()):
                if (self._scrollAtMin == 3):
                    self.parent.loadPrevImage()
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
