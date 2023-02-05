import cutlet
import argostranslate.package as package
import argostranslate.translate

from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QDialog
from PyQt5.QtCore import QThreadPool
from services import BaseWorker, State


class TranslationDialog(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.ocrLabel = QLabel("OCR")
        layout.addWidget(self.ocrLabel)

        self.ocrLineEdit = QTextEdit("")
        layout.addWidget(self.ocrLineEdit)

        self.romanjiLabel = QLabel("Romanji")
        layout.addWidget(self.romanjiLabel)

        self.romanjiLineEdit = QTextEdit("")
        layout.addWidget(self.romanjiLineEdit)

        self.translationLabel = QLabel("Translation")
        layout.addWidget(self.translationLabel)

        self.translationLineEdit = QTextEdit("")
        layout.addWidget(self.translationLineEdit)

        self.setLayout(layout)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeUtility)
        self.resize(500, 200)

        self.text = ""
        self.katakanaToRomaji = cutlet.Cutlet()
        self.state = State()
        self.threadpool = QThreadPool()
        self.loadTranslationModel()

    def loadTranslationModel(self):
        def loadArgosTranslate(state: State):
            package.update_package_index()
            from_code = "ja"
            to_code = "en"

            # Download and install Argos Translate package.
            availablePackages = argostranslate.package.get_available_packages()
            availablePackage = list(
                filter(
                    lambda x: x.from_code == from_code and x.to_code == to_code,
                    availablePackages,
                )
            )[0]
            downloadPath = availablePackage.download()
            argostranslate.package.install_from_path(downloadPath)

            # Set translation
            installedLanguages = argostranslate.translate.get_installed_languages()
            from_lang = list(
                filter(lambda x: x.code == from_code, installedLanguages)
            )[0]
            to_lang = list(filter(lambda x: x.code == to_code, installedLanguages))[0]
            state.translationModel = from_lang.get_translation(to_lang)

        worker = BaseWorker(loadArgosTranslate, self.state)
        self.threadpool.start(worker)

    def setText(self, text):
        self.text = text
        self.ocrLineEdit.setText(text)
        self.romanjiLineEdit.setText(self.katakanaToRomaji.romaji(text))
        argos_text = ""
        try:
            argos_text = self.state.translationModel.translate(text)
        except:
            print("Caught error from argos_text")
            argos_text = ""
        self.translationLineEdit.setText(argos_text)
