from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, 
                            QWidget, QAction, QTabWidget, QVBoxLayout, QGridLayout,
                            QLabel, QHBoxLayout, QFileDialog)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, pyqtSignal, pyqtSlot

import memory as mem
from viewer import ImageViewer, ImageNavigator

from default import cfg
from os.path import exists

class PMainWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.ribbon = QTabWidget()
        self.createRibbon()
        self.layout.addWidget(self.ribbon)
        
        self.img_viewer = ImageNavigator()
        self.layout.addWidget(self.img_viewer)

    def createRibbon(self):
        h = self.frameGeometry().height() * cfg["TBAR_ISIZE_REL"] * cfg["RBN_HEIGHT"]
        self.ribbon.setFixedHeight(h)
        for tab_name, tools in cfg["TBAR_FUNCS"].items():
            self.ribbon.addTab(Toolbar(parent=self, fxns=tools), tab_name)

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
        # Connect the trigger signal to a slot.
        self.img_viewer.some_signal.connect(self.handle_trigger)

        # Emit the signal.
        self.img_viewer.some_signal.emit("1")

    @pyqtSlot(str)
    def handle_trigger(self, r):
        #print("I got a signal" + r)
        pass

    def compare_img(self):
        #self.img_viewer.mask_viewer.setHidden(
        #    not self.img_viewer.mask_viewer.isHidden())
        pass

class Toolbar(QWidget):

    acquire_index = pyqtSignal(int)

    def __init__(self, parent=None, fxns=None):
        super(QWidget, self).__init__()
        self.layout = QHBoxLayout(self)
        self.buttons = []
        self.parent = parent

        s = self.parent.frameGeometry().height() * cfg["TBAR_ISIZE_REL"]
        m = s * cfg["TBAR_ISIZE_MARGIN"]
        self.layout.setAlignment(Qt.AlignLeft)
        count = 0
        for fxn in fxns:
            icon = QIcon()
            path = cfg["TBAR_IMG_ASSETS"] + fxn + ".png"
            if (exists(path)):
                icon = QIcon(path)
            else: icon = QIcon(cfg["TBAR_ICON_IMG"])
            
            self.buttons.append(QPushButton(self))
            self.buttons[-1].setIcon(icon)
            self.buttons[-1].setIconSize(QSize(s,s))
            self.buttons[-1].setFixedSize(QSize(m,m))
            #if count == 0:
            #    self.buttons.append(QPushButton(self))
            #    self.buttons[-1].setIcon(QIcon("../assets/images/" + fxn + ".png"))
            #    self.buttons[-1].setIconSize(QSize(s,s))
            #    self.buttons[-1].setFixedSize(QSize(m,m))
                #r = cfg[fxn]["button_code"]
                #print(r)
                #self.buttons[-1].clicked.connect(lambda s=r: self.on_click(s))
                #count += 1
            #else:
            #    self.buttons.append(QPushButton("", self))
            #    self.buttons[-1].setFixedSize(QSize(m,m))
            self.buttons[-1].clicked.connect(getattr(self.parent, fxn))
            self.layout.addWidget(self.buttons[-1])
    
    @pyqtSlot(str)
    def on_click(self, index):
        print("hahahaha", index)