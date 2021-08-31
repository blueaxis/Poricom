import sys

from PyQt5.QtCore import Qt, QDir, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import (QImage, QPixmap, QIcon)
from PyQt5.QtWidgets import (QWidget, QFileSystemModel, QTreeView,
                            QHBoxLayout, QMainWindow, QApplication, QPushButton, 
                            QAction, QTabWidget, QVBoxLayout, QGridLayout,
                            QLabel, QFileDialog, QScrollArea, QSizePolicy)

from GUIElements import ImageNavigator, ImageViewer, Ribbon
import memory as mem

class PMainWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.vlayout = QVBoxLayout(self)

        self.ribbon = Ribbon(self)
        self.vlayout.addWidget(self.ribbon)

        self.explorer = ImageNavigator(self)
        self.viewer = ImageViewer()

        temp_widget = QWidget()
        hlayout = QHBoxLayout(temp_widget)
        hlayout.addWidget(self.explorer)
        hlayout.addWidget(self.viewer)

        self.vlayout.addWidget(temp_widget)
    
    def load_default_img(self):
        fp = self.explorer.model.index(0, 0, 
            self.explorer.model.index(self.explorer.model.rootPath()))
        print(mem.get_curr_img())
        mem.set_curr_img(self.explorer.model.rootPath()+"/"+self.explorer.model.data(fp))
        self.viewer.view_image()

    def view_image_from_explorer(self, index):
        fp = self.explorer.model.fileInfo(index).absoluteFilePath()
        mem.set_curr_img(fp)
        self.viewer.view_image()

    def update_window(self, mode=0):
        self.img_viewer.set_proj_path(mem.get_img_path())

    def open_dir(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if path:
            mem.set_img_path(path)
            self.update_window()

    def save_img(self):
        print("Image saved to ", mem.get_img_path())
        pass

    def delete_img(self):
        print("Image deleted in ", mem.get_img_path())
        pass

    def get_mask(self):
        print("Generating mask for ", mem.get_img_path())
        pass

    def delete_text(self):
        print("Text deleted from mask ", mem.get_img_path())
        pass

    def edit_mask_(self):
        #TODO
        pass

    def edit_mask(self):
        pass
        
    def compare_img(self):
        #self.img_viewer.mask_viewer.setHidden(
        #    not self.img_viewer.mask_viewer.isHidden())
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PMainWindow()
    widget.showMaximized()
    sys.exit(app.exec_())