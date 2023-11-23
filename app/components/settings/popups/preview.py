 
from PyQt5.QtWidgets import QWidget

from .base import BaseOptions
from utils.constants import FONT_SIZE, FONT_STYLE, TOGGLE_CHOICES
from utils.scripts import editStylesheet


class PreviewOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [FONT_STYLE, FONT_SIZE, TOGGLE_CHOICES])
        self.initializeProperties(
            [
                ("estiloFuente", "  estilo-fuente: 'Helvetica';\n", str),
                ("tamanoFuente", "  tamano-fuente: 16pt;\n", str),
                ("mantenerTexto", "true", bool),
            ]
        )
        self.setOptionIndex("tamanoFuente", 2)
        self.setOptionIndex("mantenerTexto", 1)

    def changeEstiloFuente(self, i):
        self.estiloFuenteIndex = i
        selectedestiloFuente = self.estiloFuenteComboBox.currentText().strip()
        replacementText = f"  estilo-fuente: '{selectedestiloFuente}';\n"
        self.estiloFuente = replacementText

    def changetamanoFuente(self, i):
        self.tamanoFuenteIndex = i
        selectedtamanoFuente = int(self.tamanoFuenteComboBox.currentText().strip())
        replacementText = f"  tamano-fuente: {selectedtamanoFuente}pt;\n"
        self.tamanoFuente = replacementText

    def changeMantenerTexto(self, i):
        self.mantenerTextoIndex = i
        self.mantenerTexto = True if i else False

    def saveSettings(self, hasMessage=False):
        editStylesheet(41, self.estiloFuente)
        editStylesheet(42, self.tamanoFuente)
        self.mainWindow.canvas.setProperty(
            "mantenerTexto", "true" if self.mantenerTexto else "false"
        )
        return super().saveSettings(hasMessage)
