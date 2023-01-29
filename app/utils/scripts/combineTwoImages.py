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

from typing import Union

from PyQt5.QtGui import QPixmap, QPainter


def combineTwoImages(fileLeft: Union[str, QPixmap], fileRight: Union[str, QPixmap]):
    """
    Combines two image files or pixmaps to one pixmap
    """
    imageLeft, imageRight = QPixmap(fileRight), QPixmap(fileLeft)
    if imageRight.isNull():
        raise FileNotFoundError("The first file is null.")

    w = imageLeft.width() + imageRight.width()
    h = max(imageLeft.height(), imageRight.height())
    if imageLeft.isNull():
        w = imageRight.width() * 2
        h = imageRight.height()
    combinedImage = QPixmap(w, h)
    painter = QPainter(combinedImage)
    painter.drawPixmap(0, 0, imageLeft.width(), imageLeft.height(), imageLeft)
    painter.drawPixmap(
        imageLeft.width(), 0, imageRight.width(), imageRight.height(), imageRight
    )
    painter.end()

    return combinedImage
