"""
Poricom Image Processing Utility

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

from io import BytesIO
from os.path import splitext, basename
from pathlib import Path

from PyQt5.QtCore import QBuffer
from PyQt5.QtGui import QGuiApplication
from tesserocr import PyTessBaseAPI
from PIL import Image
import zipfile
import rarfile
import pdf2image

from utils.config import config

def mangaFileToImageDir(filepath):
    extract_path, extension = splitext(filepath)
    cache_path = f"./poricom_cache/{basename(extract_path)}"

    if extension in [".cbz", ".zip"]:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(cache_path)

    rarfile.UNRAR_TOOL = "utils/unrar.exe"
    if extension in [".cbr", ".rar"]:
        with rarfile.RarFile(filepath) as zip_ref:
            zip_ref.extractall(cache_path)

    if extension in [".pdf"]:
        try:
            images = pdf2image.convert_from_path(filepath)
        except pdf2image.exceptions.PDFInfoNotInstalledError:
            images = pdf2image.convert_from_path(filepath, poppler_path="poppler/Library/bin")
        for i in range(len(images)):
            filename = basename(extract_path)
            Path(cache_path).mkdir(parents=True, exist_ok=True)
            images[i].save(
                f"{cache_path}/{i+1}_{filename}.png", 'PNG')
    
    return cache_path

def pixboxToText(pixmap, lang="jpn_vert", model=None):

    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    pixmap.save(buffer, "PNG")
    bytes = BytesIO(buffer.data())

    if bytes.getbuffer().nbytes == 0:
        return

    pil_im = Image.open(bytes)
    text = ""

    if model is not None:
        text = model(pil_im)

    # PSM = 1 works most of the time except on smaller bounding boxes.
    # By smaller, we mean textboxes with less text. Usually these
    # boxes have at most one vertical line of text.
    else:
        with PyTessBaseAPI(path=config["LANG_PATH"], lang=lang, oem = 1, psm=1) as api:
            api.SetImage(pil_im)
            text = api.GetUTF8Text()

    return text.strip()

def logText(text, mode=False, path="."):
    clipboard = QGuiApplication.clipboard()
    clipboard.setText(text)

    if mode:
        with open(path, 'a', encoding="utf-8") as fh:
            fh.write(text + "\n")