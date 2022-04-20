"""
Poricom
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

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractEventDispatcher
from pyqtkeybind import keybinder

from MainWindow import PMainWindow, WinEventFilter
from Trackers import Tracker
from utils.config import cfg

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("Poricom")
    app.setWindowIcon(QIcon(cfg["LOGO"]))

    tracker = Tracker()
    widget = PMainWindow(parent=None, tracker=tracker)

    styles = cfg["STYLES_DEFAULT"]
    with open(styles, 'r') as fh:
        app.setStyleSheet(fh.read())
    
    keybinder.init()
    keybinder.register_hotkey(widget.winId(), 
        cfg["SHORTCUT"]["external_capture"], widget.capture_external)
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    widget.showMaximized()
    widget.load_model()
    app.exec_()

    keybinder.unregister_hotkey(widget.winId(), 
        cfg["SHORTCUT"]["external_capture"])
    sys.exit()