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

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from ..image import BaseImageView
from .base import BaseOCRView
from services import State
from components.popups import TranslationDialog
from os.path import join
from utils.scripts import logText
from PyQt5 import QtCore


class OCRView(BaseImageView, BaseOCRView):
    def __init__(self, parent: QMainWindow, state: State = None):
        super().__init__(parent, state)
        self.loadSettings()
        self.translationDialog = TranslationDialog()

    @pyqtSlot()
    def rubberBandStopped(self):
        super().rubberBandStopped()

    def handleTextResult(self, result):
        try:
            self.canvasText.hide()
            self.translationDialog.setText(result)
            self.translationDialog.show()
        except RuntimeError:
            pass

    def mouseReleaseEvent(self, event):
        logPath = join(self.explorerPath, "text-log.txt")
        text = self.translationDialog.text
        logText(text, isLogFile=self.logToFile, path=logPath)
        try:
            if not self.persistText:
                self.canvasText.hide()
        except AttributeError:
            pass
        super(BaseOCRView, self).mouseReleaseEvent(event)

    def closeEvent(self, event):
        self.translationDialog.close()
