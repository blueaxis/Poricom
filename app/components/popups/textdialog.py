import cutlet
import argostranslate.package as package
import argostranslate.translate

from PyQt5.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QDialog
from PyQt5 import QtCore

class TextDialog(QDialog):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label_ocr = QLabel("OCR")
        layout.addWidget(self.label_ocr)

        self.line_edit_ocr = QTextEdit("")
        layout.addWidget(self.line_edit_ocr)

        self.label_romanji = QLabel("Romanji")
        layout.addWidget(self.label_romanji)

        self.line_edit_romanji = QTextEdit("")
        layout.addWidget(self.line_edit_romanji)

        self.label_translation= QLabel("Translation")
        layout.addWidget(self.label_translation)

        self.line_edit_translation = QTextEdit("")
        layout.addWidget(self.line_edit_translation)

        self.setLayout(layout)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeUtility)
        self.resize(500, 200)


        self.text = ""
        self.ktkn2romanji = cutlet.Cutlet()
        package.update_package_index()
        from_code = "ja"
        to_code = "en"
        
        # Download and install Argos Translate package.
        available_packages = argostranslate.package.get_available_packages()
        available_package = list(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            )
        )[0]
        download_path = available_package.download()
        argostranslate.package.install_from_path(download_path)

        # Set translation
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = list(filter(
                lambda x: x.code == from_code,
                installed_languages))[0]
        to_lang = list(filter(
                lambda x: x.code == to_code,
                installed_languages))[0]
        self.translation = from_lang.get_translation(to_lang)

    
    def setText(self, text):
        self.text = text
        self.line_edit_ocr.setText(text)
        self.line_edit_romanji.setText(self.ktkn2romanji.romaji(text))
        argos_text = ""
        try:
            argos_text = self.translation.translate(text)
        except:
            print("Caught error from argos_text")
            argos_text = ""
        self.line_edit_translation.setText(argos_text)