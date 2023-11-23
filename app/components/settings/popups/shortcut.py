from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget

from .base import BaseOptions
from components.popups import BasePopup
from utils.constants import MODIFIER


class ShortcutOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [MODIFIER])
        self.initializeProperties([("modifier", "Alt", str)])
        self.setOptionIndex("modifier", 2)
        self.addDefaults(
            {"captureExternalKey": "Q", "captureExternalShortcut": "Alt+Q"}
        )
        self.loadSettings()

        self.keyLineEdit = QLineEdit(self.captureExternalKey)
        self.layout().addWidget(self.keyLineEdit, 1, 1)
        self.layout().addWidget(QLabel("Tecla: "), 1, 0)

    def raiseKeyInvalidError(self, message: str):
        BasePopup("Tecla Inválida", message).exec()

    def changeModifier(self, i):
        self.modifierIndex = i
        self.modifier = self.modifierComboBox.currentText().strip() + "+"
        if self.modifier == "Sin Modificador+":
            self.modifier = ""

    def changeShortcut(self):
        self.captureExternalShortcut = self.modifier + self.captureExternalKey

    def saveSettings(self, hasMessage=False):
        if not self.keyLineEdit.text().isalnum():
            self.raiseKeyInvalidError("Please select an alphanumeric key.")
            return
        if len(self.keyLineEdit.text()) != 1:
            self.raiseKeyInvalidError("Please select exactly one key.")
            return
        self.captureExternalKey = self.keyLineEdit.text()

        self.changeShortcut()

        super().saveSettings(hasMessage)

        BasePopup("Shortcut Remapped", "Close the app to apply changes.").exec()
