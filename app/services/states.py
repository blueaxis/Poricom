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
from requests import post
from typing import Literal

from argostranslate.package import (
    get_available_packages,
    install_from_path,
    update_package_index,
)
from argostranslate.translate import get_installed_languages
from manga_ocr import MangaOcr
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPixmap

from utils.constants import SETTINGS_FILE_DEFAULT, TRANSLATE_MODEL
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
TranslateModelNames = Literal["ArgosTranslate", "ChatGPT", "DeepL"]


class State:
    def __init__(self):
        self._baseImage = Pixmap("")

        settings = QSettings(SETTINGS_FILE_DEFAULT, QSettings.IniFormat)

        ocrModelName = settings.value("ocrModel", "MangaOCR")
        self._ocrModel = None
        self._ocrModelName: OCRModelNames = ocrModelName

        translateModelIndex = settings.value("translateModelIndex", 0)
        translateModelName = TRANSLATE_MODEL[int(translateModelIndex)].strip()
        translateApiKey = settings.value("translateApiKey", "")
        self._translateModel = None
        self._translateModelName: TranslateModelNames = translateModelName
        self._translateApiKey = translateApiKey

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
            self._ocrModel = None
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

    # ---------------------------------- Translate ---------------------------------- #

    @property
    def translateModel(self):
        return self._translateModel

    @translateModel.setter
    def translateModel(self, translateModel):
        self._translateModel = translateModel

    @property
    def translateModelName(self):
        return self._translateModelName

    def setTranslateModelName(self, translateModelName: TranslateModelNames = None):
        self._translateModelName = translateModelName
        return self._translateModelName

    @property
    def translateApiKey(self):
        return self._translateApiKey

    def setTranslateApiKey(self, translateApiKey):
        self._translateApiKey = translateApiKey
        return self._translateApiKey

    def downloadArgosTranslateModel(self, fromCode="ja", toCode="en"):
        update_package_index()
        availablePackages = get_available_packages()
        availablePackage = list(
            filter(
                lambda x: x.from_code == fromCode and x.to_code == toCode,
                availablePackages,
            )
        )[0]
        downloadPath = availablePackage.download()
        install_from_path(downloadPath)

    def getArgosTranslateModel(self, fromCode="ja", toCode="en"):
        installedLanguages = get_installed_languages()
        fromLang = list(filter(lambda x: x.code == fromCode, installedLanguages))
        toLang = list(filter(lambda x: x.code == toCode, installedLanguages))

        if not fromLang or not toLang:
            return None
        return fromLang[0], toLang[0]

    def loadTranslateModel(self):
        if self._translateModelName == "ArgosTranslate":
            languages = self.getArgosTranslateModel()
            if languages:
                fromLang, toLang = languages
                self.translateModel = fromLang.get_translation(toLang)
            else:
                self.downloadArgosTranslateModel()
                languages = self.getArgosTranslateModel()
                if not languages:
                    return "Error while loading offline model."
                fromLang, toLang = languages
                self.translateModel = fromLang.get_translation(toLang)
            return "success"
        else:
            self.translateModel = None
            return "success"

    def predictTranslate(self, text):
        if self.translateModelName == "ArgosTranslate":
            return self.translateModel.translate(text)
        elif self.translateModelName == "ChatGPT":
            headers = {
                "content-type": "application/json",
                "authorization": f"Bearer {self.translateApiKey}",
            }
            body = {
                "model": "text-davinci-003",
                "prompt": f"Translate this to English:\n{text}",
                "temperature": 0.3,
                "max_tokens": 128,
            }
            response = post(
                "https://api.openai.com/v1/completions", json=body, headers=headers
            ).json()
            try:
                return response["choices"][0]["text"].strip()
            except Exception as e:
                return text
        elif self.translateModelName == "DeepL":
            headers = {
                "content-type": "application/json",
                "authorization": f"DeepL-Auth-Key {self.translateApiKey}",
            }
            body = {
                "text": text,
                "target_lang": "EN",
            }
            response = post(
                "https://api-free.deepl.com/v2/translate", json=body, headers=headers
            ).json()
            try:
                return response["translations"]["text"].strip()
            except Exception as e:
                return text
