
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from MainWindow import PMainWindow
from Trackers import Tracker

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("Poricom")
    app.setWindowIcon(QIcon("../assets/images/icons/logo.png"))

    tracker = Tracker()
    widget = PMainWindow(parent=None, tracker=tracker)
    
    styles = "../assets/styles.qss"
    with open(styles, 'r') as fh:
        app.setStyleSheet(fh.read())

    widget.showMaximized()
    sys.exit(app.exec_())