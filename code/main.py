import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import PMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PMainWindow()
    widget.showMaximized()
    sys.exit(app.exec_())