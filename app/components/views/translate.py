import cutlet
from PyQt5.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget


class TranslateView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ocrLineEdit = QTextEdit("")
        self.romajiLineEdit = QTextEdit("")
        self.translateLineEdit = QTextEdit("")

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Detected Text"))
        self.layout().addWidget(self.ocrLineEdit)
        self.layout().addWidget(QLabel("Romaji"))
        self.layout().addWidget(self.romajiLineEdit)
        self.layout().addWidget(QLabel("Translation"))
        self.layout().addWidget(self.translateLineEdit)

        self.katakanaToRomaji = cutlet.Cutlet()

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
