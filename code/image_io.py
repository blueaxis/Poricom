from PyQt5.QtCore import QBuffer
from PIL import Image
from io import BytesIO

import pytesseract
#from tesserocr import PyTessBaseAPI, PSM

# TODO: use tesserocr instead
def pixmap_to_text(pixmap):

    lang = "eng"
    oem = 1
    psm = 1
    config = f"-l {lang} --oem {oem} --psm {psm}"

    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    pixmap.save(buffer, "PNG")
    pil_im = Image.open(BytesIO(buffer.data()))

    # Filter text first
    text = pytesseract.image_to_string(pil_im, config=(config))
    print(text)
    print("EOL")