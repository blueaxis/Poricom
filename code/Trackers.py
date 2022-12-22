"""
Poricom State-Tracking Logic

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

from os.path import isfile, join, splitext, normpath, abspath, exists, dirname
from os import listdir

from PyQt5.QtGui import QPixmap, QPainter

from utils.config import config


class Tracker:

    def __init__(self, filename=config["HOME_IMAGE"], filenext=config["ABOUT_IMAGE"]):
        if not config["SPLIT_VIEW_MODE"]:
            self._pixImage = PImage(filename)
        if config["SPLIT_VIEW_MODE"]:
            splitImage = self.twoFileToImage(filename, filenext)
            self._pixImage = PImage(splitImage, filename)
        self._pixMask = PImage(filename)

        self._filepath = abspath(dirname(filename))
        self._writeMode = False

        self._imageList = []

        self._language = "jpn"
        self._orientation = "_vert"

        self._betterOCR = False
        self._ocrModel = None

    def twoFileToImage(self, fileLeft, fileRight):
        imageLeft, imageRight = PImage(fileRight), PImage(fileLeft)
        if not (imageLeft.isValid()):
            return

        w = imageLeft.width() + imageRight.width()
        h = max(imageLeft.height(), imageRight.height())
        if imageRight.isNull():
            w = imageLeft.width() * 2
            h = imageLeft.height()
        splitImage = QPixmap(w, h)
        painter = QPainter(splitImage)
        painter.drawPixmap(0, 0, imageLeft.width(), imageLeft.height(),
                           imageLeft)
        painter.drawPixmap(imageLeft.width(), 0, imageRight.width(),
                           imageRight.height(), imageRight)
        painter.end()

        return splitImage

    @property
    def pixImage(self):
        return self._pixImage

    @pixImage.setter
    def pixImage(self, image):
        if (type(image) is str and PImage(image).isValid()):
            self._pixImage = PImage(image)
            self._pixImage.filename = abspath(image)
            self._filepath = abspath(dirname(image))
        if (type(image) is tuple):
            fileLeft, fileRight = image
            if not fileRight:
                if fileLeft:
                    self._pixImage = PImage(fileLeft)
                    self._pixImage.filename = abspath(fileLeft)
                    self._filepath = abspath(dirname(fileLeft))
                return
            splitImage = self.twoFileToImage(fileLeft, fileRight)

            self._pixImage = PImage(splitImage, fileLeft)
            self._pixImage.filename = abspath(fileLeft)
            self._filepath = abspath(dirname(fileLeft))

    @property
    def pixMask(self):
        return self._pixMask

    @pixMask.setter
    def pixMask(self, image):
        self._pixMask = image

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepath):
        self._filepath = filepath
        filelist = filter(lambda f: isfile(join(self.filepath,
                                                f)), listdir(self.filepath))
        self._imageList = list(map(lambda p: normpath(join(self.filepath, p)), filter(
            (lambda f: ('*'+splitext(f)[1]) in config["IMAGE_EXTENSIONS"]), filelist)))

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        self._orientation = orientation

    @property
    def ocrModel(self):
        return self._ocrModel

    @ocrModel.setter
    def ocrModel(self, ocrModel):
        self._ocrModel = ocrModel

    @property
    def writeMode(self):
        return self._writeMode

    @writeMode.setter
    def writeMode(self, writeMode):
        self._writeMode = writeMode

    def switchWriteMode(self):
        self._writeMode = not self._writeMode
        return self._writeMode

    def switchOCRMode(self):
        self._betterOCR = not self._betterOCR
        return self._betterOCR


class PImage(QPixmap):

    def __init__(self, *args):
        super(QPixmap, self).__init__(args[0])

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
