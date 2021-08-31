import sys

from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QGridLayout, 
                            QWidget, QFileDialog)

from GUIElements import ImageNavigator, ImageViewer, Ribbon
from default import cfg
import memory as mem

class PMainWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        vlayout = QVBoxLayout(self)

        self.ribbon = Ribbon(self)
        vlayout.addWidget(self.ribbon)

        self.explorer = ImageNavigator(self)
        self.viewer = ImageViewer()

        main_widget = QWidget()
        self.hlayout = QHBoxLayout(main_widget)
        self.init_main_widget()

        vlayout.addWidget(main_widget)

    def init_main_widget(self):
        self.hlayout.addWidget(self.explorer, cfg["NAV_VIEW_RATIO"][0])
        self.hlayout.addWidget(self.viewer, cfg["NAV_VIEW_RATIO"][1])

        self.hlayout.setContentsMargins(0,0,2,0)

    def load_default_img(self):
        fp = self.explorer.model.index(0, 0, 
            self.explorer.model.index(self.explorer.model.rootPath()))
        mem.set_curr_img(self.explorer.model.rootPath()+"/"+self.explorer.model.data(fp))
        self.viewer.view_image()

    def view_image_from_explorer(self, index):
        fp = self.explorer.model.fileInfo(index).absoluteFilePath()
        mem.set_curr_img(fp)
        self.viewer.view_image()

    def update_window(self, mode=0):
        self.explorer.set_proj_path(mem.get_img_path())

    def open_dir(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if path:
            mem.set_img_path(path)
            self.explorer.set_proj_path(mem.get_img_path())

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