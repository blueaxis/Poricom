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

from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QPushButton, 
                            QMessageBox, QFileDialog, QInputDialog, QMainWindow)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from manga_ocr import MangaOcr

from Trackers import Tracker
from GUIElements import (ImageNavigator, Ribbon, OCRCanvas, 
                        BaseWorker, BaseThread)
from default import cfg

class LoadModelWorker(BaseWorker):

    @pyqtSlot(Tracker)
    def run(self, tracker):
        better_ocr = tracker.switch_ocr_mode()
        if better_ocr:
            tracker.ocr_model = MangaOcr()
        else:
            tracker.ocr_model = None
        self.finished.emit()

class PMainWindow(QMainWindow):
    # TODO: add pyqtSlot decorator that will update
    # all GUI elements on the window

    runLoadModel = pyqtSignal(Tracker)

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__(parent)
        self.tracker = tracker
        self.vlayout = QVBoxLayout()

        self.ribbon = Ribbon(self, self.tracker)
        self.vlayout.addWidget(self.ribbon)
        self.canvas = OCRCanvas(self, self.tracker)
        self.explorer = ImageNavigator(self, self.tracker)

        self._view_widget = QWidget()
        hlayout = QHBoxLayout(self._view_widget)
        hlayout.addWidget(self.explorer, cfg["NAV_VIEW_RATIO"][0])
        hlayout.addWidget(self.canvas, cfg["NAV_VIEW_RATIO"][1])
        hlayout.setContentsMargins(0,0,0,0)

        self.vlayout.addWidget(self._view_widget)
        _main_widget = QWidget()
        _main_widget.setLayout(self.vlayout)
        self.setCentralWidget(_main_widget)

    @pyqtSlot()
    def loadModelHelper(self):
        self.runLoadModel.emit(self.tracker)

    def view_image_from_explorer(self, filename): 
        self.tracker.p_image = filename
        if not self.tracker.p_image.is_valid():
            return False
        self.canvas.viewImage()
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
            self.explorer.setDirectory(filepath)

    def open_manga(self):
        return

    def toggle_logging(self):
        self.tracker.switch_write_mode()

    def toggle_mouse_mode(self):
        self.canvas.toggleZoomPanMode()

    def load_model(self):
        load_model_btn = self.ribbon.findChild(QPushButton, "load_model")
        load_model_btn.setChecked(not self.tracker.ocr_model)

        if load_model_btn.isChecked():
            confirmation = QMessageBox(QMessageBox.NoIcon, 
                "Load the MangaOCR model?", 
                "If you are running this for the first time, this will " + 
                "download the MangaOcr model which is about 400 MB in size. " + 
                "This will improve the accuracy of Japanese text detection " + 
                "in Poricom. If it is already in your cache, it will take a " +
                "few seconds to load the model.",
                QMessageBox.Ok | QMessageBox.Cancel)
            ret = confirmation.exec()
            if (ret == QMessageBox.Ok):
                pass
            else:
                load_model_btn.setChecked(False)
                return

        self.worker = LoadModelWorker()
        self.thread = BaseThread(self.worker, self.loadModelHelper,
                              self.confirm_load_model, self.runLoadModel)
        self.worker.moveToThread(self.thread)
        self.thread.start()

        load_model_btn.setEnabled(False)
        self.thread.finished.connect(lambda: load_model_btn.setEnabled(True))

    def load_prev_image(self):
        index = self.explorer.indexAbove(self.explorer.currentIndex())
        if (not index.isValid()):
            return
        self.explorer.setCurrentIndex(index)

    def load_next_image(self):
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

    def zoom_in(self):
        return

    def zoom_out(self):
        return

    def confirm_load_model(self):
        model_name = "MangaOCR" if self.tracker.ocr_model else "Tesseract"
        QMessageBox(QMessageBox.NoIcon, 
            f"{model_name} model loaded", 
            f"You are now using the {model_name} model for Japanese text detection.",
            QMessageBox.Ok).exec()