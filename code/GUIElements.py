from PyQt5.QtCore import Qt, QDir, QSize
from PyQt5.QtGui import (QImage, QPixmap, QIcon)
from PyQt5.QtWidgets import (QGridLayout, QWidget, QFileSystemModel, 
                            QTreeView, QPushButton, QTabWidget, 
                            QLabel, QScrollArea, QHBoxLayout)

import memory as mem
from default import cfg
from os.path import exists

class ImageNavigator(QTreeView):

    def __init__(self, parent=None):
        super(QTreeView, self).__init__()
        self.parent = parent

        self.model = QFileSystemModel()
        self.init_fs_model()

        self.setModel(self.model)
        self.init_treeview()

        self.set_proj_path(mem.get_img_path())
        self.selectionModel().selectionChanged.connect(self.jump_to_item)

    def init_fs_model(self):
        self.model.setFilter(QDir.Files)
        self.model.setNameFilterDisables(False)
        self.model.setNameFilters(cfg["IMAGE_EXTENSIONS"])

        self.model.directoryLoaded.connect(
            getattr(self.parent, cfg["NAV_FUNCS"]["path_changed"]))

    def init_treeview(self):
        for i in range(1,4):
            self.hideColumn(i)
        self.setIndentation(5)
        #self.setSortingEnabled(True)

        # add entered signal maybe?
        self.clicked.connect(
            getattr(self.parent, cfg["NAV_FUNCS"]["nav_clicked"]))

    def set_proj_path(self, path):
        if path is None:
            #TODO: Error Handling
            pass
        if (path != cfg["NAV_ROOT"]):
            pass
        mem.set_img_path(path)
        self.setRootIndex(self.model.setRootPath(path))

    def jump_to_item(self, selected, deselected):
        #print("Jump")
        pass

class ImageViewer(QScrollArea):
    def __init__(self, parent = None):
        super(QScrollArea, self).__init__(parent)

        self._img_label = QLabel()
        self.setWidget(self._img_label)
        self.init_img_label()

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        #self.verticalScrollBar().valueChanged.connect(lambda idx: self.scrolling_temp(idx))

    def init_img_label(self):
        self._img_label.setContentsMargins(10,10,10,0)

    def view_image(self, filepath=None, q_image=None, mode=0):

        w = self.frameGeometry().width()
        h = self.frameGeometry().height()

        filepath = mem.get_curr_img()
        image = q_image
        if filepath:
            image = QImage(filepath)
            if image is None:
                #TODO: Error Handling
                return
        pixmap_img = QPixmap.fromImage(image)
        self._img_label.setPixmap(pixmap_img.scaledToWidth(
                        w-20, Qt.SmoothTransformation))
        self._img_label.adjustSize()
    
    def resizeEvent(self, event):
        self.view_image()
        QScrollArea.resizeEvent(self, event)
    
    def scrolling_temp(self,idx):
        pass
        #print(idx)

class PageNavigator(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.button_list = []

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        for func_name, func_cfg in cfg["MODE_FUNCS"].items():
            self.load_button_config(func_name, func_cfg)

        self.layout.addWidget(self.button_list[0], 0, 0, 1, 2)
        self.layout.addWidget(self.button_list[1], 1, 0) 
        self.layout.addWidget(self.button_list[2], 1, 1, alignment=Qt.AlignRight)

    def load_button_config(self, b_name, b_config):
    
        w = self.parent.frameGeometry().height()*cfg["TBAR_ISIZE_REL"]*b_config["icon_w"]
        h = self.parent.frameGeometry().height()*cfg["TBAR_ISIZE_REL"]*b_config["icon_h"]
        m = cfg["TBAR_ISIZE_MARGIN"]

        icon = QIcon()
        path = b_config["path"]
        if (exists(path)):
            icon = QIcon(path)
        else: icon = QIcon(cfg["TBAR_ICON_IMG"])

        self.button_list.append(QPushButton(self))
        self.button_list[-1].setIcon(icon)
        self.button_list[-1].setIconSize(QSize(w,h))
        self.button_list[-1].setFixedSize(QSize(w*m,h*m))

        self.button_list[-1].setToolTip(b_config["help_msg"])
        self.button_list[-1].setCheckable(b_config["toggle"])

        self.button_list[-1].clicked.connect(getattr(self.parent, b_name))

class Toolbar(QWidget):

    def __init__(self, parent=None, funcs=None, aob_exists=False):
        super(QWidget, self).__init__()
        self.parent = parent

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)
        self.button_list = []
        self.aob_exists = aob_exists

        self.init_buttons(funcs)
    
    def init_buttons(self, funcs):

        for func_name, func_cfg in funcs.items():
            self.load_button_config(func_name, func_cfg)
        self.layout.addStretch()
        aob = PageNavigator(self.parent)
        self.layout.addWidget(aob)
    
    def load_button_config(self, b_name, b_config):

        s = self.parent.frameGeometry().height()*cfg["TBAR_ISIZE_REL"]#*b_config["is_half"]
        m = s * cfg["TBAR_ISIZE_MARGIN"]

        icon = QIcon()
        path = b_config["path"]
        if (exists(path)):
            icon = QIcon(path)
        else: icon = QIcon(cfg["TBAR_ICON_IMG"])

        #TODO: add keyboard shortcut using name scheme
        self.button_list.append(QPushButton(self))
        self.button_list[-1].setIcon(icon)
        self.button_list[-1].setIconSize(QSize(s,s))
        self.button_list[-1].setFixedSize(QSize(m,m))

        self.button_list[-1].setToolTip(b_config["help_msg"])
        self.button_list[-1].setCheckable(b_config["toggle"])

        self.button_list[-1].clicked.connect(getattr(self.parent, b_name))
        self.layout.addWidget(self.button_list[-1], 
            alignment=getattr(Qt, b_config["align"]))

class Ribbon(QTabWidget):
    def __init__(self, parent=None):
        super(QTabWidget, self).__init__(parent) #remove parent?
        self.parent = parent
        h = self.parent.frameGeometry().height() * cfg["TBAR_ISIZE_REL"] * cfg["RBN_HEIGHT"]
        self.setFixedHeight(h)
        #TODO: add keyboard shortcut using name scheme
        for tab_name, tools in cfg["TBAR_FUNCS"].items():
            self.addTab(Toolbar(parent=self.parent, funcs=tools), tab_name)

