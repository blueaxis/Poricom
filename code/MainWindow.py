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

from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget,
                            QPushButton, QFileDialog, QInputDialog)
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from manga_ocr import MangaOcr
from Trackers import Tracker

from GUIElements import ImageNavigator, Ribbon, OCRCanvas
from default import cfg

class Worker(QObject):
    finished = pyqtSignal()

    @pyqtSlot(Tracker)
    def run(self, tracker):
        better_ocr = tracker.switch_ocr_mode()
        if better_ocr:
            tracker.ocr_model = MangaOcr()
        else:
            tracker.ocr_model = None
        self.finished.emit()

class PMainWindow(QWidget):
    # TODO: add pyqtSlot decorator that will update
    # all GUI elements on the window

    runLoadModel = pyqtSignal(Tracker)

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__(parent)
        self.tracker = tracker

        vlayout = QVBoxLayout(self)

        self.ribbon = Ribbon(self, self.tracker)
        vlayout.addWidget(self.ribbon)

        self.canvas = OCRCanvas(self, self.tracker)
        self.explorer = ImageNavigator(self, self.tracker)

        main_widget = QWidget()
        self.hlayout = QHBoxLayout(main_widget)
        self.hlayout.addWidget(self.explorer, cfg["NAV_VIEW_RATIO"][0])
        self.hlayout.addWidget(self.canvas, cfg["NAV_VIEW_RATIO"][1])

        # Ribbon is off by 2 pixels on my machine
        # Might need to check this on another pc
        self.hlayout.setContentsMargins(0,0,2,0)

        vlayout.addWidget(main_widget)        

    @pyqtSlot()
    def loadModelHelper(self):
        self.runLoadModel.emit(self.tracker)

    def view_image_from_explorer(self, filename): 
        self.tracker.p_image = filename
        if not self.tracker.p_image.is_valid():
            return False
        self.canvas.view_image()
        return True

    def open_dir(self):
        filepath = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            "." # , QFileDialog.DontUseNativeDialog
        )

        if filepath:
            # self.tracker.p_image = filename
            self.tracker.filepath = filepath
            self.explorer.set_directory(filepath)

    def toggle_logging(self):
        self.tracker.switch_write_mode()

    def load_model(self):

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.loadModelHelper)
        self.runLoadModel.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.start()

        load_model_btn = self.ribbon.findChild(QPushButton, "load_model")
        load_model_btn.setEnabled(False)
        self.thread.finished.connect(lambda: load_model_btn.setEnabled(True))

    def load_prev_image(self):
        # change gray to blue selection
        index = self.explorer.indexAbove(self.explorer.currentIndex())
        if (not index.isValid()):
            return
        self.explorer.setCurrentIndex(index)

    def load_next_image(self):
        # change gray to blue selection
        index = self.explorer.indexBelow(self.explorer.currentIndex())
        if (not index.isValid()):
            return
        self.explorer.setCurrentIndex(index)

    def load_image_at_idx(self):
        row_count = self.explorer.model.rowCount(self.explorer.rootIndex())
        i, _ = QInputDialog.getInt(
            self, 
            'Jump to', 
            f'Enter page number: (max is {row_count})',
            value = -1,
            min = 1,
            max = row_count,
            flags = Qt.CustomizeWindowHint| Qt.WindowTitleHint)
        if (i == -1):
            return

        index = self.explorer.model.index(i-1, 0, self.explorer.rootIndex())
        self.explorer.setCurrentIndex(index)