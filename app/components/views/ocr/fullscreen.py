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

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QMainWindow
from PyQt5.QtGui import QCursor, QMouseEvent

from .base import BaseOCRView
from utils.constants import TESSERACT_DEFAULTS, TEXT_LOGGING_DEFAULTS


class FullScreenOCRView(BaseOCRView):
    """
    Fullscreen view with OCR capabilities
    """

    def __init__(self, parent: QMainWindow, tracker=None):
        super().__init__(parent, tracker)
        self.externalWindow = parent

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setScene(QGraphicsScene())
        self.loadSettings({**TESSERACT_DEFAULTS, **TEXT_LOGGING_DEFAULTS})

    def takeScreenshot(self, screenIndex: int):
        screen = QApplication.screens()[screenIndex]
        s = screen.size()
        self.pixmap = self.scene().addPixmap(
            screen.grabWindow(0).scaled(s.width(), s.height())
        )
        self.scene().setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def getActiveScreenIndex(self):
        cursor = QCursor.pos()
        return QApplication.desktop().screenNumber(cursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        self.externalWindow.close()
