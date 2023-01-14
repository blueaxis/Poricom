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

from PyQt5.QtCore import (pyqtSlot, Qt, QThreadPool, QTimer)
from PyQt5.QtWidgets import (QGraphicsView, QLabel, QMainWindow)

from components.services import BaseWorker
from utils.image_io import logText, pixboxToText


class BaseOCRView(QGraphicsView):
    """Base view with OCR capabilities

    Args:
        parent (QMainWindow): View parent. Set to main window
        tracker (Any, optional): State tracker. Defaults to None.
    """
    def __init__(self, parent: QMainWindow, tracker=None):
        # TODO: Remove references to tracker
        super().__init__(parent)
        self.tracker = tracker

        self.timer = QTimer()
        self.timer.setInterval(300)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.rubberBandStopped)

        self.canvasText = QLabel("", self, Qt.WindowStaysOnTopHint)
        self.canvasText.setWordWrap(True)
        self.canvasText.hide()
        self.canvasText.setObjectName("canvasText")

        self.setDragMode(QGraphicsView.RubberBandDrag)

    def handleTextResult(self, result):
        try:
            self.canvasText.setText(result)
        except RuntimeError:
            pass
    
    def handleTextFinished(self):
        try:
            self.canvasText.adjustSize()
        except RuntimeError:
            pass
        try:
            self.timer.timeout.connect(self.rubberBandStopped)
        except TypeError:
            pass

    @pyqtSlot()
    def rubberBandStopped(self):

        if (self.canvasText.isHidden()):
            self.canvasText.setText("")
            self.canvasText.adjustSize()
            self.canvasText.show()

        lang = self.tracker.language + self.tracker.orientation
        pixbox = self.grab(self.rubberBandRect())

        worker = BaseWorker(pixboxToText, pixbox, lang, self.tracker.ocrModel)
        worker.signals.result.connect(self.handleTextResult)
        worker.signals.finished.connect(self.handleTextFinished)
        self.timer.timeout.disconnect(self.rubberBandStopped)
        QThreadPool.globalInstance().start(worker)

    def mouseMoveEvent(self, event):
        rubberBandVisible = not self.rubberBandRect().isNull()
        if (event.buttons() & Qt.LeftButton) and rubberBandVisible:
            self.timer.start()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        logPath = self.tracker.filepath + "/log.txt"
        logToFile = self.tracker.writeMode
        text = self.canvasText.text()
        logText(text, mode=logToFile, path=logPath)
        try:
            if not self.parent().config["PERSIST_TEXT_MODE"]:
                self.canvasText.hide()
        except AttributeError:
            pass
        super().mouseReleaseEvent(event)
