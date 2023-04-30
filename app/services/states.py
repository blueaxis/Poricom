"""
Poricom States

Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from os.path import isfile, exists
from typing import Literal

from manga_ocr import MangaOcr
from PyQt5.QtGui import QPixmap

from utils.scripts import combineTwoImages


class Pixmap(QPixmap):
    def __init__(self, *args):
        super().__init__(args[0])

        # Current directory + filename
        if type(args[0]) == str:
            self._filename = args[0]
        if type(args[0]) == QPixmap:
            self._filename = args[1]
        # Current directory
        self._filepath = None

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    def isValid(self):
        return exists(self._filename) and isfile(self._filename)


OCRModelNames = Literal["Tesseract", "MangaOCR"]


class State:
    def __init__(self):
        self._baseImage = Pixmap("")

        self._ocrModel = None
        self._ocrModelName: OCRModelNames = "Tesseract"

    # ------------------------------------ Image ------------------------------------ #

    @property
    def baseImage(self):
        return self._baseImage

    @baseImage.setter
    def baseImage(self, image):
        if type(image) is str and Pixmap(image).isValid():
            self._baseImage = Pixmap(image)
        if type(image) is tuple:
            fileLeft, fileRight = image
            if not fileRight:
                if fileLeft:
                    self._baseImage = Pixmap(fileLeft)
                return
            splitImage = combineTwoImages(fileLeft, fileRight)

            self._baseImage = Pixmap(splitImage, fileLeft)

    # ------------------------------------- OCR ------------------------------------- #

    @property
    def ocrModel(self):
        return self._ocrModel

    @ocrModel.setter
    def ocrModel(self, ocrModel):
        self._ocrModel = ocrModel

    @property
    def ocrModelName(self):
        return self._ocrModelName

    def setOCRModelName(self, ocrModelName: OCRModelNames = None):
        if ocrModelName:
            self._ocrModelName = ocrModelName
        else:
            self.toggleOCRModelName()
        return self._ocrModelName

    def toggleOCRModelName(self):
        if self._ocrModelName == "Tesseract":
            self._ocrModelName = "MangaOCR"
        elif self._ocrModelName == "MangaOCR":
            self._ocrModelName = "Tesseract"
        return self._ocrModelName

    def loadOCRModel(self, path: str = None):
        if self._ocrModelName == "Tesseract":
            return "success"
        elif self._ocrModelName == "MangaOCR":
            try:
                if path:
                    self.ocrModel = MangaOcr(pretrained_model_name_or_path=path)
                else:
                    self.ocrModel = MangaOcr()
                return "success"
            except Exception as e:
                self.setOCRModelName("Tesseract")
                return str(e)
