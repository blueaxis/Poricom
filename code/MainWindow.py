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

from shutil import rmtree
from time import sleep

import toml
from manga_ocr import MangaOcr
from PyQt5.QtCore import (Qt, QAbstractNativeEventFilter, QThreadPool)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QPushButton, 
                            QFileDialog, QInputDialog, QMainWindow, QApplication)

from Workers import BaseWorker
from GUIElements import (ImageNavigator, OCRCanvas, FullScreen)
from Ribbon import Ribbon
from Popups import (FontPicker, LanguagePicker, ScaleImagePicker, ShortcutPicker, 
                    PickerPopup, MessagePopup)
from image_io import mangaFileToImageDir
from utils.config import config, saveOnClose

class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

class PMainWindow(QMainWindow):
    # TODO: add pyqtSlot decorator that will update
    # all GUI elements on the window

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__(parent)
        self.tracker = tracker
        self.config= config

        self.vlayout = QVBoxLayout()
        self.ribbon = Ribbon(self, self.tracker)
        self.vlayout.addWidget(self.ribbon)
        self.canvas = OCRCanvas(self, self.tracker)
        self.explorer = ImageNavigator(self, self.tracker)

        self._view_widget = QWidget()
        hlayout = QHBoxLayout(self._view_widget)
        hlayout.addWidget(self.explorer, config["NAV_VIEW_RATIO"][0])
        hlayout.addWidget(self.canvas, config["NAV_VIEW_RATIO"][1])
        hlayout.setContentsMargins(0,0,0,0)

        self.vlayout.addWidget(self._view_widget)
        _main_widget = QWidget()
        _main_widget.setLayout(self.vlayout)
        self.setCentralWidget(_main_widget)

        self.threadpool = QThreadPool()

    def view_image_from_explorer(self, filename, filenext):
        if not self.canvas.splitViewMode():
            self.tracker.p_image = filename
        if self.canvas.splitViewMode():
            self.tracker.p_image = (filename, filenext)
        if not self.tracker.p_image.is_valid():
            return False
        self.canvas.resetTransform()
        self.canvas.currentScale = 1
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
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Manga File",
            ".",
            "Manga (*.cbz *.cbr *.zip *.rar *.pdf)"
        )

        if filename:
            def setDirectory(filepath):
                self.tracker.filepath = filepath
                self.explorer.setDirectory(filepath)

            open_manga_btn = self.ribbon.findChild(
                QPushButton, "open_manga")

            worker = BaseWorker(mangaFileToImageDir, filename)
            worker.signals.result.connect(setDirectory)
            worker.signals.finished.connect(lambda: 
                open_manga_btn.setEnabled(True))

            self.threadpool.start(worker)
            open_manga_btn.setEnabled(False)

    def capture_external_helper(self):
        self.showMinimized()
        sleep(0.5)
        if self.isMinimized():
            self.capture_external()

    def capture_external(self):
        ext_window = QMainWindow()
        ext_window.layout().setContentsMargins(0, 0, 0, 0)
        ext_window.setStyleSheet("border:0px; margin:0px")

        ext_window.setCentralWidget(FullScreen(ext_window, self.tracker))
        ext_window.centralWidget().takeScreenshot()
        ext_window.showFullScreen()

    def toggle_stylesheet(self):
        config = "./utils/config.toml"
        light_mode = "./assets/styles.qss"
        dark_mode = "./assets/styles-dark.qss"

        data = toml.load(config)
        if data["STYLES_DEFAULT"] == light_mode:
            data["STYLES_DEFAULT"] = dark_mode
        elif data["STYLES_DEFAULT"] == dark_mode:
            data["STYLES_DEFAULT"] = light_mode
        with open(config, 'w') as fh:
            toml.dump(data, fh)

        app = QApplication.instance()
        if app is None:
            raise RuntimeError("No Qt Application found.")

        styles = data["STYLES_DEFAULT"]
        config["STYLES_DEFAULT"] = data["STYLES_DEFAULT"]
        with open(styles, 'r') as fh:
            app.setStyleSheet(fh.read())

    def modify_font_settings(self):
        confirmation = PickerPopup(FontPicker(self, self.tracker))
        ret = confirmation.exec()

        if ret:
            app = QApplication.instance()
            if app is None:
                raise RuntimeError("No Qt Application found.")

            with open(config["STYLES_DEFAULT"], 'r') as fh:
                app.setStyleSheet(fh.read())

    def toggle_split_view(self):
        self.canvas.toggleSplitView()
        if self.canvas.splitViewMode():
            self.canvas.setViewImageMode(2)
            index = self.explorer.currentIndex()
            self.explorer.currentChanged(index, index)
        elif not self.canvas.splitViewMode():
            index = self.explorer.currentIndex()
            self.explorer.currentChanged(index, index)

    def scale_image(self):
        confirmation = PickerPopup(ScaleImagePicker(self, self.tracker))
        confirmation.exec()

    def toggle_mouse_mode(self):
        self.canvas.toggleZoomPanMode()

    def modify_hotkeys(self):
        confirmation = PickerPopup(ShortcutPicker(self, self.tracker))
        ret = confirmation.exec()
        if ret:
            MessagePopup(
                "Shortcut Remapped",
                "Close the app to apply changes."
            ).exec()

    def load_model(self):
        load_model_btn = self.ribbon.findChild(QPushButton, "load_model")
        load_model_btn.setChecked(not self.tracker.ocr_model)

        if load_model_btn.isChecked():
            confirmation = MessagePopup(
                "Load the MangaOCR model?", 
                "If you are running this for the first time, this will " + 
                "download the MangaOcr model which is about 400 MB in size. " + 
                "This will improve the accuracy of Japanese text detection " + 
                "in Poricom. If it is already in your cache, it will take a " +
                "few seconds to load the model.",
                MessagePopup.Ok | MessagePopup.Cancel
            )
            ret = confirmation.exec()
            if (ret == MessagePopup.Ok):
                pass
            else:
                load_model_btn.setChecked(False)
                return

        def loadModelHelper(tracker):
            better_ocr = tracker.switch_ocr_mode()
            if better_ocr:
                import http.client as httplib
                def isConnected(url="8.8.8.8"):
                    connection = httplib.HTTPSConnection(url, timeout=2)
                    try:
                        connection.request("HEAD", "/")
                        return True
                    except Exception:
                        return False
                    finally:
                        connection.close()

                connected = isConnected()
                if connected:
                    tracker.ocr_model = MangaOcr()
                return (better_ocr, connected)
            else:
                tracker.ocr_model = None
                return (better_ocr, True)

        def modelLoadedConfirmation(type_connection_tuple):
            using_manga_ocr, connected = type_connection_tuple
            model_name = "MangaOCR" if using_manga_ocr else "Tesseract"
            if connected:
                MessagePopup(
                    f"{model_name} model loaded",
                    f"You are now using the {model_name} model for Japanese text detection."
                ).exec()
                
            elif not connected:
                MessagePopup(
                    "Connection Error",
                    "Please try again or make sure your Internet connection is on."
                ).exec()
                load_model_btn.setChecked(False)

        worker = BaseWorker(loadModelHelper, self.tracker)
        worker.signals.result.connect(modelLoadedConfirmation)
        worker.signals.finished.connect(lambda: 
            load_model_btn.setEnabled(True))

        self.threadpool.start(worker)
        load_model_btn.setEnabled(False)

    def modify_tesseract(self):
        confirmation = PickerPopup(LanguagePicker(self, self.tracker))
        confirmation.exec()

    def toggle_logging(self):
        self.tracker.switch_write_mode()

    def load_prev_image(self):
        index = self.explorer.indexAbove(self.explorer.currentIndex())
        if self.canvas.splitViewMode():
            tempIndex = self.explorer.indexAbove(index)
            if tempIndex.isValid():
                index = tempIndex
        if (not index.isValid()):
            return
        self.explorer.setCurrentIndex(index)

    def load_next_image(self):
        index = self.explorer.indexBelow(self.explorer.currentIndex())
        if self.canvas.splitViewMode():
            tempIndex = self.explorer.indexBelow(index)
            if tempIndex.isValid():
                index = tempIndex
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
        self.canvas.zoomView(True, usingButton=True)

    def zoom_out(self):
        self.canvas.zoomView(False, usingButton=True)

    def closeEvent(self, event):
        try:
            rmtree("./poricom_cache")
        except FileNotFoundError:
            pass
        saveOnClose(self.config)
        return QMainWindow.closeEvent(self, event)
    
    def poricomNoop(self):
        MessagePopup(
            "WIP",
            "This function is not yet implemented."
        ).exec()
