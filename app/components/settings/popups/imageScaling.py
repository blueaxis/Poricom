 
from PyQt5.QtWidgets import QWidget

from .base import BaseOptions
from utils.constants import IMAGE_SCALING


class ImageScalingOptions(BaseOptions):
    def __init__(self, parent: QWidget):
        super().__init__(parent, [IMAGE_SCALING])
        # TODO: Use constants here
        # TODO: Image scaling must be an enum not an int
        self.initializeProperties([("imageScaling", 0, int)])

    def changeImageScaling(self, i):
        self.imageScalingIndex = i

    def saveSettings(self, hasMessage=False):
        self.mainWindow.canvas.modifyViewImageMode(self.imageScalingIndex)
        return super().saveSettings(hasMessage)
