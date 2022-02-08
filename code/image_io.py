from io import BytesIO

from PyQt5.QtCore import QBuffer
from PIL import Image
from PyQt5.QtGui import QGuiApplication
from tesserocr import PyTessBaseAPI

def pixbox_to_text(pixmap, lang="jpn_vert"):

    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    pixmap.save(buffer, "PNG")
    pil_im = Image.open(BytesIO(buffer.data()))
    text = ""

    # PSM = 1 works most of the time except on smaller bounding boxes.
    # By smaller, we mean textboxes with less text. Usually these
    # boxes have at most one vertical line of text.
    with PyTessBaseAPI(path="../assets/languages/", lang=lang, oem = 1, psm=1) as api:
        api.SetImage(pil_im)
        text = api.GetUTF8Text()

    text = text.replace("\n", " ")

    clipboard = QGuiApplication.clipboard()
    clipboard.setText(text)

    # allow writing to a log file

    return text