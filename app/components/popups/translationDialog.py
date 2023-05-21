import cutlet
from PyQt5.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt

from services import State


class TranslationDialog(QDialog):
    def __init__(self, parent=None, state: State = None):
        super().__init__(parent, flags=Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose | Qt.WA_X11NetWmWindowTypeUtility)

        self.setLayout(QVBoxLayout())
        self.ocrLineEdit = QTextEdit("")
        self.romajiLineEdit = QTextEdit("")
        self.translateLineEdit = QTextEdit("")
        self.layout().addWidget(QLabel("Detected Text"))
        self.layout().addWidget(self.ocrLineEdit)
        self.layout().addWidget(QLabel("Romaji"))
        self.layout().addWidget(self.romajiLineEdit)
        self.layout().addWidget(QLabel("Translation"))
        self.layout().addWidget(self.translateLineEdit)
        self.resize(500, 200)

        self.text = ""
        self.katakanaToRomaji = cutlet.Cutlet()
        self.state = state

    def setText(self, text):
        self.text = text
        self.ocrLineEdit.setText(text)
        try:
            romajiText = self.katakanaToRomaji.romaji(text)
        except Exception as e:
            print(e)
            romajiText = ""
        try:
            argosText = self.state.predictTranslate(text)
        except Exception as e:
            print(e)
            argosText = ""
        self.romajiLineEdit.setText(romajiText)
        self.translateLineEdit.setText(argosText)
