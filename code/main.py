
import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import PMainWindow
from Trackers import Tracker

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tracker = Tracker()
    widget = PMainWindow(parent=None, tracker=tracker)
    widget.showMaximized()
    sys.exit(app.exec_())