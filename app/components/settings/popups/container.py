 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from .base import BaseOptions


class OptionsContainer(QDialog):
    """Dialog to contain option widgets

    Args:
        options (BaseOptions): Child option widget
    """

    def __init__(self, options: BaseOptions):
        super().__init__(
            None,
            Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint,
        )
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.options = options
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(options)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout().addWidget(self.buttonBox)

        self.buttonBox.rejected.connect(self.cancelClickedEvent)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        self.options.saveSettings(hasMessage=False)
        return super().accept()

    def cancelClickedEvent(self):
        self.close()

    def closeEvent(self, event):
        self.options.close()
        return super().closeEvent(event)
