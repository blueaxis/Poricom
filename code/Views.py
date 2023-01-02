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

from time import sleep

from PyQt5.QtCore import (Qt, QRectF, QTimer, QThreadPool, pyqtSlot)
from PyQt5.QtCore import (Qt, QRect, QSize, QRectF,
                          QTimer, QThreadPool, pyqtSlot)
from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QLabel)

from Workers import BaseWorker
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
        self.canvasText.setWordWrap(True)
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
        try:
            if not self.parent.config["PERSIST_TEXT_MODE"]:
                self.canvasText.hide()
        except AttributeError:
            pass
        super().mouseReleaseEvent(event)

    @pyqtSlot()
    def rubberBandStopped(self):

        if (self.canvasText.isHidden()):
            self.canvasText.setText("")
            self.canvasText.adjustSize()
            self.canvasText.show()

        lang = self.tracker.language + self.tracker.orientation
        pixbox = self.grab(self.rubberBandRect())

        worker = BaseWorker(pixboxToText, pixbox, lang, self.tracker.ocrModel)
        worker.signals.result.connect(self.canvasText.setText)
        worker.signals.finished.connect(self.canvasText.adjustSize)
        self.timer_.timeout.disconnect(self.rubberBandStopped)
        worker.signals.finished.connect(
            lambda: self.timer_.timeout.connect(self.rubberBandStopped))
        QThreadPool.globalInstance().start(worker)


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
        self._trackPadAtMin = 0
        self._trackPadAtMax = 0
        self._scrollSuppressed = False

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(self.tracker.pixImage.scaledToWidth(
            self.viewport().geometry().width(), Qt.SmoothTransformation))

    def viewImage(self, factor=1):
        # self.verticalScrollBar().setSliderPosition(0)
        factor = self.currentScale
        w = factor*self.viewport().geometry().width()
        h = factor*self.viewport().geometry().height()
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
            #self.scale(factor, factor)
            self.currentScale *= factor
            self.viewImage(self.currentScale)
        elif not isZoomIn and self.currentScale > 0.35:
            #self.scale(1/factor, 1/factor)
            self.currentScale /= factor
            self.viewImage(self.currentScale)

    def toggleZoomPanMode(self):
        self._zoomPanMode = not self._zoomPanMode

    def resizeEvent(self, event):
        self.viewImage()
        QGraphicsView.resizeEvent(self, event)

    def wheelEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        zoomMode = pressedKey == Qt.ControlModifier or self._zoomPanMode

        # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if zoomMode:
            if event.angleDelta().y() > 0:
                isZoomIn = True
            elif event.angleDelta().y() < 0:
                isZoomIn = False
            scenePos = self.mapToScene(event.pos())
            truePos = QRect(scenePos.toPoint(), QSize(2, 2)).center()
            self.centerOn(truePos)
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
        self.currentScale = 1
        self.viewImage(self.currentScale)
        QGraphicsView.mouseDoubleClickEvent(self, event)
