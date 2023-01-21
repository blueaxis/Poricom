"""
Poricom Windows

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
from PyQt5.QtCore import (Qt, QThreadPool)
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QDesktopWidget, QMainWindow, QApplication,
                             QPushButton, QFileDialog)

from components.services import BaseWorker
from components.settings import PreviewOptions, ImageScalingOptions, OptionsContainer, TesseractOptions
from components.toolbar import BaseToolbar
from components.views import WorkspaceView, FullScreenOCRView
from Popups import (ShortcutPicker, PickerPopup, MessagePopup, CheckboxPopup)
from utils.config import config, saveOnClose
from utils.constants import LOAD_MODEL_MESSAGE
from utils.scripts import mangaFileToImageDir


class MainWindow(QMainWindow):

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__(parent)
        self.tracker = tracker
        self.config = config

        self.vLayout = QVBoxLayout()

        self.mainView = WorkspaceView(self, self.tracker)
        self.ribbon = BaseToolbar(self)
        self.vLayout.addWidget(self.ribbon)

        self.vLayout.addWidget(self.mainView)
        _mainWidget = QWidget()
        _mainWidget.setLayout(self.vLayout)
        self.setCentralWidget(_mainWidget)

        self.threadpool = QThreadPool()

    @property
    def canvas(self):
        return self.mainView.canvas
    
    @property
    def explorer(self):
        return self.mainView.explorer

    def closeEvent(self, event):
        try:
            rmtree("./poricom_cache")
        except FileNotFoundError:
            pass
        self.config["NAV_ROOT"] = self.tracker.filepath
        saveOnClose(self.config)
        return QMainWindow.closeEvent(self, event)

    def poricomNoop(self):
        MessagePopup(
            "WIP",
            "This function is not yet implemented."
        ).exec()

# ------------------------------ File Functions ------------------------------ #

    def openDir(self):
        filepath = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            self.tracker.filepath  # , QFileDialog.DontUseNativeDialog
        )

        if filepath:
            try:
                self.tracker.filepath = filepath
                self.explorer.setDirectory(filepath)
            except FileNotFoundError:
                MessagePopup(
                    f"No images found in the directory",
                    f"Please select a directory with images."
                ).exec()

    def openManga(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Manga File",
            self.tracker.filepath,
            "Manga (*.cbz *.cbr *.zip *.rar *.pdf)"
        )

        if filename:
            def setDirectory(filepath):
                self.tracker.filepath = filepath
                self.explorer.setDirectory(filepath)

            openMangaButton = self.ribbon.findChild(
                QPushButton, "openManga")

            worker = BaseWorker(mangaFileToImageDir, filename)
            worker.signals.result.connect(setDirectory)
            worker.signals.finished.connect(
                lambda: openMangaButton.setEnabled(True))

            self.threadpool.start(worker)
            openMangaButton.setEnabled(False)

    def captureExternalHelper(self):
        self.showMinimized()
        sleep(0.5)
        if self.isMinimized():
            self.captureExternal()

    def captureExternal(self):
        externalWindow = QMainWindow()
        externalWindow.layout().setContentsMargins(0, 0, 0, 0)
        externalWindow.setStyleSheet("border:0px; margin:0px")
        externalWindow.setAttribute(Qt.WA_DeleteOnClose)

        externalWindow.setCentralWidget(
            FullScreenOCRView(externalWindow, self.tracker))
        fullScreen = externalWindow.centralWidget()

        screenIndex = fullScreen.getActiveScreenIndex()
        screen = QDesktopWidget().screenGeometry(screenIndex)
        fullScreen.takeScreenshot(screenIndex)
        externalWindow.move(screen.left(), screen.top())
        externalWindow.showFullScreen()

# ------------------------------ View Functions ------------------------------ #

    def toggleStylesheet(self):
        config = "./utils/config.toml"
        lightMode = "./assets/styles.qss"
        darkMode = "./assets/styles-dark.qss"

        data = toml.load(config)
        if data["STYLES_DEFAULT"] == lightMode:
            data["STYLES_DEFAULT"] = darkMode
        elif data["STYLES_DEFAULT"] == darkMode:
            data["STYLES_DEFAULT"] = lightMode
        with open(config, 'w') as fh:
            toml.dump(data, fh)

        app = QApplication.instance()
        if app is None:
            raise RuntimeError("No Qt Application found.")

        styles = data["STYLES_DEFAULT"]
        self.config["STYLES_DEFAULT"] = data["STYLES_DEFAULT"]
        with open(styles, 'r') as fh:
            app.setStyleSheet(fh.read())

    def modifyFontSettings(self):
        confirmation = OptionsContainer(PreviewOptions(self))
        ret = confirmation.exec()

        if ret:
            app = QApplication.instance()
            if app is None:
                raise RuntimeError("No Qt Application found.")

            with open(config["STYLES_DEFAULT"], 'r') as fh:
                app.setStyleSheet(fh.read())

    def toggleSplitView(self):
        self.canvas.toggleSplitView()
        if self.canvas.splitViewMode:
            self.canvas.setViewImageMode(2)
            index = self.explorer.currentIndex()
            self.explorer.currentChanged(index, index)
        elif not self.canvas.splitViewMode:
            index = self.explorer.currentIndex()
            self.explorer.currentChanged(index, index)

    def scaleImage(self):
        confirmation = OptionsContainer(ImageScalingOptions(self))
        confirmation.exec()

    def hideExplorer(self):
        self.explorer.setVisible(not self.explorer.isVisible())

# ----------------------------- Control Functions ---------------------------- #

    def toggleMouseMode(self):
        self.canvas.toggleZoomPanMode()

    def modifyHotkeys(self):
        confirmation = PickerPopup(ShortcutPicker(self, self.tracker))
        ret = confirmation.exec()
        if ret:
            MessagePopup(
                "Shortcut Remapped",
                "Close the app to apply changes."
            ).exec()

# ------------------------------ Misc Functions ------------------------------ #

    def loadModel(self):
        loadModelButton = self.ribbon.findChild(QPushButton, "loadModel")
        loadModelButton.setChecked(not self.tracker.ocrModel)

        if loadModelButton.isChecked() and self.config["LOAD_MODEL_POPUP"]:
            confirmation = CheckboxPopup(
                "Load the MangaOCR model?",
                LOAD_MODEL_MESSAGE,
                MessagePopup.Ok | MessagePopup.Cancel
            )
            ret = confirmation.exec()
            self.config["LOAD_MODEL_POPUP"] = not confirmation.checkBox().isChecked()
            if (ret == MessagePopup.Ok):
                pass
            else:
                loadModelButton.setChecked(False)
                return

        def loadModelHelper(tracker):
            betterOCR = tracker.switchOCRMode()
            if betterOCR:
                try:
                    tracker.ocrModel = MangaOcr()
                    return "success"
                except Exception as e:
                    tracker.switchOCRMode()
                    return str(e)
            else:
                tracker.ocrModel = None
                return "success"

        def loadModelConfirm(message: str):
            modelName = "MangaOCR" if self.tracker.ocrModel else "Tesseract"
            if message == "success":
                MessagePopup(
                    f"{modelName} model loaded",
                    f"You are now using the {modelName} model for Japanese text detection."
                ).exec()
            else:
                MessagePopup("Load Model Error", message).exec()
                loadModelButton.setChecked(False)

        worker = BaseWorker(loadModelHelper, self.tracker)
        worker.signals.result.connect(loadModelConfirm)
        worker.signals.finished.connect(lambda:
                                        loadModelButton.setEnabled(True))

        self.threadpool.start(worker)
        loadModelButton.setEnabled(False)

    def modifyTesseract(self):
        confirmation = OptionsContainer(TesseractOptions(self))
        confirmation.exec()
        if confirmation:
            self.canvas.loadSettings()

    def toggleLogging(self):
        self.tracker.switchWriteMode()
