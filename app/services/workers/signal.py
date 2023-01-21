"""
Poricom Services

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

from PyQt5.QtCore import pyqtSignal, QObject


class BaseWorkerSignal(QObject):
    """Base signal object

    Signals:
        finished: Emit when thread finished the task
        result: Emit the result of the task
    """

    finished = pyqtSignal()
    result = pyqtSignal(object)
