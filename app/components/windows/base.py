 

import re
from shutil import rmtree
from time import sleep

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .external import ExternalWindow
from components.popups import BasePopup, CheckboxPopup
from components.settings import (
    BaseSettings,
    ModelOptions,
    OptionsContainer,
    PreviewOptions,
    ShortcutOptions,
    TranslateOptions,
)
from components.toolbar import BaseToolbar
from components.views import WorkspaceView
from services import BaseWorker, State
from utils.constants import (
    LOAD_MODEL_MESSAGE,
    MAIN_WINDOW_DEFAULTS,
    MAIN_WINDOW_TYPES,
    PORICOM_CACHE,
    STYLESHEET_DARK,
    STYLESHEET_LIGHT,
    TRANSLATE_DEFAULTS,
    TRANSLATE_TYPES,
)


class MainWindow(QMainWindow, BaseSettings):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.state = State()

        self.vLayout = QVBoxLayout()

        self.mainView = WorkspaceView(self, self.state)
        self.toolbar = BaseToolbar(self)
        self.vLayout.addWidget(self.toolbar)

        self.vLayout.addWidget(self.mainView)
        mainWidget = QWidget()
        mainWidget.setLayout(self.vLayout)
        self.setCentralWidget(mainWidget)

        self.setDefaults({**MAIN_WINDOW_DEFAULTS, **TRANSLATE_DEFAULTS})
        self.setTypes({**MAIN_WINDOW_TYPES, **TRANSLATE_TYPES})
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
            rmtree(PORICOM_CACHE)
        except FileNotFoundError:
            pass
        self.saveSettings(False)
        self.mainView.saveSettings(False)
        self.canvas.close()
        return super().closeEvent(event)

    def noop(self):
        BasePopup("Not Implemented", "This function is not yet implemented.").exec()

    # ------------------------------- File Functions -------------------------------- #

    def captureExternalHelper(self):
        self.showMinimized()
        sleep(0.5)
        if self.isMinimized():
            self.captureExternal()

    def captureExternal(self):
        ExternalWindow(self).showFullScreen()

    # ------------------------------- View Functions -------------------------------- #

    def toggleStylesheet(self):
        if self.stylesheetPath == STYLESHEET_LIGHT:
            self.stylesheetPath = STYLESHEET_DARK
        elif self.stylesheetPath == STYLESHEET_DARK:
            self.stylesheetPath = STYLESHEET_LIGHT

        app = QApplication.instance()
        if app is None:
            raise RuntimeError("Ninguna aplicación qt fue encontrada.")

        with open(self.stylesheetPath, "r") as fh:
            app.setStyleSheet(fh.read())

    def modifyFontSettings(self):
        confirmation = OptionsContainer(PreviewOptions(self))
        ret = confirmation.exec()

        if ret:
            app = QApplication.instance()
            if app is None:
                raise RuntimeError("Ninguna aplicación qt fue encontrada.")

            with open(self.stylesheetPath, "r") as fh:
                app.setStyleSheet(fh.read())

    # ------------------------------ Control Functions ------------------------------ #

    def modifyHotkeys(self):
        OptionsContainer(ShortcutOptions(self)).exec()

    # ------------------------------- Misc Functions -------------------------------- #

    def loadModel(self):
        confirmation = OptionsContainer(ModelOptions(self))
        confirmed = confirmation.exec()

        if confirmed:
            self.loadSettings({"usarOCRoffline": "false"})
        if self.usarOCRoffline and not self.mangaOCRPath:
            startPath = self.mainView.explorerPath or "."
            ocrPath = QFileDialog.getExistingDirectory(
                self, "Definir Directorio de MangaOCR", startPath
            )
            if ocrPath:
                self.mangaOCRPath = ocrPath
        elif not self.usarOCRoffline:
            self.mangaOCRPath = ""

        if confirmed:
            self.loadModelAfterPopup()

    def loadModelAfterPopup(self):
        loadModelButton = self.toolbar.findChild(QPushButton, "loadModel")
        isMangaOCR = self.state.ocrModelName == "MangaOCR"

        if not isMangaOCR:
            return

        if isMangaOCR and self.hasLoadModelPopup:
            ret = CheckboxPopup(
                "hasLoadModelPopup",
                "¿Cargar los archivos del OCR?",
                LOAD_MODEL_MESSAGE,
                CheckboxPopup.Ok | CheckboxPopup.Cancelar,
            ).exec()
            if ret == CheckboxPopup.Cancelar:
                return
            self.loadSettings({"hasLoadModelPopup": "true"})

        def loadModelConfirm(message: str):
            modelName = self.state.ocrModelName
            if message == "success":
                BasePopup(
                    f"{modelName} ha sido cargado.",
                    f"Ahora estás usando el modelo {modelName} de detección de texto.",
                ).exec()
            else:
                BasePopup("Load Model Error", message).exec()
                if re.search(
                    "^unable to parse .* as a URL or as a local path$", message
                ):
                    self.mangaOCRPath = ""

        worker = BaseWorker(self.state.loadOCRModel, self.mangaOCRPath)
        worker.signals.result.connect(loadModelConfirm)
        worker.signals.finished.connect(lambda: loadModelButton.setEnabled(True))

        self.threadpool.start(worker)
        loadModelButton.setEnabled(False)

    def loadTranslateModel(self):
        confirmation = OptionsContainer(TranslateOptions(self))
        confirmed = confirmation.exec()
        if confirmed:
            self.loadSettings(TRANSLATE_DEFAULTS)
            self.canvas.loadSettings(TRANSLATE_DEFAULTS)
            self.loadTranslateAfterPopup()

    def loadTranslateAfterPopup(self):
        loadModelButton = self.toolbar.findChild(QPushButton, "loadTranslateModel")
        if not self.enableTranslate:
            self.mainView.translateView.hide()
            return

        worker = BaseWorker(self.state.loadTranslateModel)
        worker.signals.finished.connect(lambda: loadModelButton.setEnabled(True))

        self.threadpool.start(worker)
        loadModelButton.setEnabled(False)

    def toggleLogging(self):
        self.logToFile = not self.logToFile
        self.canvas.loadSettings()
