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

from manga_ocr import MangaOcr
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QApplication,
    QPushButton,
    QFileDialog,
)

from .external import ExternalWindow
from components.popups import BasePopup, CheckboxPopup
from components.services import BaseWorker
from components.settings import (
    BaseSettings,
    PreviewOptions,
    ImageScalingOptions,
    OptionsContainer,
    ShortcutOptions,
    TesseractOptions,
)
from components.toolbar import BaseToolbar
from components.views import WorkspaceView
from utils.constants import (
    LOAD_MODEL_MESSAGE,
    MAIN_WINDOW_DEFAULTS,
    MAIN_WINDOW_TYPES,
    STYLESHEET_DARK,
    STYLESHEET_LIGHT,
)
from utils.scripts import mangaFileToImageDir


class MainWindow(QMainWindow, BaseSettings):
    def __init__(self, parent=None, tracker=None):
        super().__init__(parent)
        self.tracker = tracker

        self.vLayout = QVBoxLayout()

        self.mainView = WorkspaceView(self, self.tracker)
        self.toolbar = BaseToolbar(self)
        self.vLayout.addWidget(self.toolbar)

        self.vLayout.addWidget(self.mainView)
        mainWidget = QWidget()
        mainWidget.setLayout(self.vLayout)
        self.setCentralWidget(mainWidget)

        self.setDefaults(MAIN_WINDOW_DEFAULTS)
        self.setTypes(MAIN_WINDOW_TYPES)
        self.loadSettings()

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
        self.saveSettings(False)
        return super().closeEvent(event)

    def noop(self):
        BasePopup("Not Implemented", "This function is not yet implemented.").exec()

    # ------------------------------ File Functions ------------------------------ #

    def openDir(self):
        filepath = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            self.tracker.filepath,  # , QFileDialog.DontUseNativeDialog
        )

        if filepath:
            try:
                self.tracker.filepath = filepath
                self.explorer.setDirectory(filepath)
                self.explorerPath = filepath
            except FileNotFoundError:
                BasePopup(
                    "No images found in the directory",
                    "Please select a directory with images.",
                ).exec()

    def openManga(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Manga File",
            self.tracker.filepath,
            "Manga (*.cbz *.cbr *.zip *.rar *.pdf)",
        )

        if filename:

            def setDirectory(filepath):
                self.tracker.filepath = filepath
                self.explorer.setDirectory(filepath)

            openMangaButton = self.toolbar.findChild(QPushButton, "openManga")

            worker = BaseWorker(mangaFileToImageDir, filename)
            worker.signals.result.connect(setDirectory)
            worker.signals.finished.connect(lambda: openMangaButton.setEnabled(True))

            self.threadpool.start(worker)
            openMangaButton.setEnabled(False)

    def captureExternalHelper(self):
        self.showMinimized()
        sleep(0.5)
        if self.isMinimized():
            self.captureExternal()

    def captureExternal(self):
        ExternalWindow(self).showFullScreen()

    # ------------------------------ View Functions ------------------------------ #

    def toggleStylesheet(self):
        if self.stylesheetPath == STYLESHEET_LIGHT:
            self.stylesheetPath = STYLESHEET_DARK
        elif self.stylesheetPath == STYLESHEET_DARK:
            self.stylesheetPath = STYLESHEET_LIGHT

        app = QApplication.instance()
        if app is None:
            raise RuntimeError("No Qt Application found.")

        with open(self.stylesheetPath, "r") as fh:
            app.setStyleSheet(fh.read())

    def modifyFontSettings(self):
        confirmation = OptionsContainer(PreviewOptions(self))
        ret = confirmation.exec()

        if ret:
            app = QApplication.instance()
            if app is None:
                raise RuntimeError("No Qt Application found.")

            with open(self.stylesheetPath, "r") as fh:
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
        OptionsContainer(ShortcutOptions(self)).exec()

    # ------------------------------ Misc Functions ------------------------------ #

    def loadModel(self):
        loadModelButton = self.toolbar.findChild(QPushButton, "loadModel")
        loadModelButton.setChecked(not self.tracker.ocrModel)

        if loadModelButton.isChecked() and self.hasLoadModelPopup:
            ret = CheckboxPopup(
                "hasLoadModelPopup",
                "Load the MangaOCR model?",
                LOAD_MODEL_MESSAGE,
                CheckboxPopup.Ok | CheckboxPopup.Cancel,
            ).exec()
            if ret == CheckboxPopup.Ok:
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
                BasePopup(
                    f"{modelName} model loaded",
                    f"You are now using the {modelName} model for Japanese text detection.",
                ).exec()
            else:
                BasePopup("Load Model Error", message).exec()
                loadModelButton.setChecked(False)

        worker = BaseWorker(loadModelHelper, self.tracker)
        worker.signals.result.connect(loadModelConfirm)
        worker.signals.finished.connect(lambda: loadModelButton.setEnabled(True))

        self.threadpool.start(worker)
        loadModelButton.setEnabled(False)

    def modifyTesseract(self):
        confirmation = OptionsContainer(TesseractOptions(self))
        confirmation.exec()
        if confirmation:
            self.canvas.loadSettings()

    def toggleLogging(self):
        self.tracker.switchWriteMode()
