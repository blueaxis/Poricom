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

from os.path import join

from PyQt5.QtCore import pyqtSlot, Qt, QThreadPool, QTimer
from PyQt5.QtWidgets import QGraphicsView, QLabel, QMainWindow

from components.popups import BasePopup, TranslationDialog
from components.settings import BaseSettings
from services import BaseWorker, State
from utils.constants import (
    TESSERACT_DEFAULTS,
    TEXT_LOGGING_DEFAULTS,
    TEXT_LOGGING_TYPES,
)
from utils.scripts import copyToClipboard, logText, pixmapToText


class BaseOCRView(QGraphicsView, BaseSettings):
    """
    Base view with OCR capabilities
    """

    def __init__(self, parent: QMainWindow, state: State = None):
        super().__init__(parent)
        self.state = state

        self.timer = QTimer()
        self.timer.setInterval(300)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.rubberBandStopped)

        self.previousSelection = self.rubberBandRect()

        self.canvasText = QLabel("", self, Qt.WindowStaysOnTopHint)
        self.canvasText.setWordWrap(True)
        self.canvasText.hide()
        self.canvasText.setObjectName("canvasText")

        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.translationDialog = TranslationDialog()

        self.addDefaults({**TESSERACT_DEFAULTS, **TEXT_LOGGING_DEFAULTS})
        self.addTypes(TEXT_LOGGING_TYPES)
        self.addProperty("persistText", "true", bool)
        self.addProperty("enableTranslate", "false", bool)

    def handleTextResult(self, result):
        if result == None and self.state.ocrModelName == "Tesseract":
            BasePopup(
                "Tesseract not loaded",
                "Tesseract model cannot be loaded in your machine, please use the MangaOcr instead.",
            ).exec()
            return
        try:
            self.canvasText.setText(result)
            self.canvasText.adjustSize()
            if self.canvasText.isHidden():
                self.canvasText.show()
        except RuntimeError:
            pass

    def handleTextFinished(self):
        try:
            self.canvasText.adjustSize()
            copyToClipboard(self.canvasText.text())
        except RuntimeError:
            pass
        try:
            self.timer.timeout.connect(self.rubberBandStopped)
        except TypeError:
            pass

    @pyqtSlot()
    def rubberBandStopped(self):
        language = self.language + self.orientation
        selection = (
            self.previousSelection
            if self.rubberBandRect().isNull()
            else self.rubberBandRect()
        )
        pixmap = self.grab(selection)

        worker = BaseWorker(pixmapToText, pixmap, language, self.state.ocrModel)
        worker.signals.result.connect(self.handleTextResult)
        worker.signals.finished.connect(self.handleTextFinished)
        self.timer.timeout.disconnect(self.rubberBandStopped)
        QThreadPool.globalInstance().start(worker)

    def mouseMoveEvent(self, event):
        rubberBandVisible = not self.rubberBandRect().isNull()
        if (event.buttons() & Qt.LeftButton) and rubberBandVisible:
            self.previousSelection = self.rubberBandRect()
            self.timer.start()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        logPath = join(self.explorerPath, "text-log.txt")
        text = self.canvasText.text()
        if self.logToFile:
            logText(text, path=logPath)

        if self.enableTranslate:
            self.translationDialog.setSourceText(text)
            worker = BaseWorker(self.state.predictTranslate, text)
            worker.signals.result.connect(self.translationDialog.setTranslateText)
            worker.signals.finished.connect(self.translationDialog.show)
            QThreadPool.globalInstance().start(worker)

        try:
            if not self.persistText:
                self.canvasText.hide()
        except AttributeError:
            pass
        super().mouseReleaseEvent(event)
