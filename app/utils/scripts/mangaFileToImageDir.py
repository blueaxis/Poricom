"""
Poricom Helper Functions

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

from os.path import splitext, basename
from pathlib import Path
from utils.constants import PORICOM_CACHE

import zipfile
import rarfile
import pdf2image


def mangaFileToImageDir(filepath: str):
    """Converts a manga file to a directory of images

    Args:
        filepath (str): Path to manga file.

    Returns:
        str: Path to directory of images.
    """
    extractPath, extension = splitext(filepath)
    cachePath = f"{PORICOM_CACHE}/{basename(extractPath)}"

    if extension in [".cbz", ".zip"]:
        with zipfile.ZipFile(filepath, "r") as zipRef:
            zipRef.extractall(cachePath)

    rarfile.UNRAR_TOOL = "bin/unrar.exe"
    if extension in [".cbr", ".rar"]:
        with rarfile.RarFile(filepath) as zipRef:
            zipRef.extractall(cachePath)

    if extension in [".pdf"]:
        try:
            images = pdf2image.convert_from_path(filepath)
        except pdf2image.exceptions.PDFInfoNotInstalledError:
            images = pdf2image.convert_from_path(
                filepath, poppler_path="poppler/Library/bin"
            )
        for i in range(len(images)):
            filename = basename(extractPath)
            Path(cachePath).mkdir(parents=True, exist_ok=True)
            images[i].save(f"{cachePath}/{i+1}_{filename}.png", "PNG")

    return cachePath
