import cutlet
from PyQt5.QtWidgets import QLabel, QTextEdit, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from utils.constants import TRANSLATE_ITEM_ORIENTATION


class TranslateView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ocrLineEdit = QTextEdit("")
        self.romajiLineEdit = QTextEdit("")
        self.translateLineEdit = QTextEdit("")
        self.detectedTextLabel = QLabel("Detected Text")
        self.romajiLabel = QLabel("Romaji")
        self.translationLabel = QLabel("Translation")

        self.setLayout(QGridLayout())
        self.setLayoutDirection(Qt.LeftToRight)
        self.layout().addWidget(self.detectedTextLabel, 0, 0)
        self.layout().addWidget(self.ocrLineEdit, 0, 1)
        self.layout().addWidget(self.romajiLabel, 0, 2)
        self.layout().addWidget(self.romajiLineEdit, 0, 3)
        self.layout().addWidget(self.translationLabel, 0, 4)
        self.layout().addWidget(self.translateLineEdit, 0, 5)

        self.katakanaToRomaji = cutlet.Cutlet()

    def changeLayout(self, layout):
        widgets = [
            self.layout().itemAt(i).widget() for i in range(self.layout().count())
        ]
        for w in widgets:
            w.setParent(None)
        i = 0
        if layout == TRANSLATE_ITEM_ORIENTATION.HORIZONTAL:
            for w in widgets:
                self.layout().addWidget(w, i, 0)
                i += 1
        elif layout == TRANSLATE_ITEM_ORIENTATION.VERTICAL:
            for w in widgets:
                self.layout().addWidget(w, 0, i)
                i += 1

    def setSourceText(self, text: str):
        self.ocrLineEdit.setText(text)
        try:
            romajiText = self.katakanaToRomaji.romaji(text)
        except Exception as e:
            print(e)
            romajiText = ""
        self.romajiLineEdit.setText(romajiText)

    def setTranslateText(self, text: str):
        self.translateLineEdit.setText(text)
