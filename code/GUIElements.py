from PyQt5.QtCore import Qt, QDir, QSize
from PyQt5.QtGui import (QImage, QPixmap, QIcon)
from PyQt5.QtWidgets import (QWidget, QFileSystemModel, QTreeView,
                            QPushButton, QTabWidget, QLabel, QFileDialog, 
                            QScrollArea, QSizePolicy, QHBoxLayout)

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

    def init_fs_model(self):
        self.model.setFilter(QDir.Files)
        self.model.setNameFilterDisables(False)
        self.model.setNameFilters(cfg["IMAGE_EXTENSIONS"])

        self.model.directoryLoaded.connect(
            getattr(self.parent, cfg["NAV_FUNCS"]["path_changed"]))
        #self.model.rootPathChanged.connect(self.set_proj_path)

    def init_treeview(self):
        for i in range(1,4):
            self.hideColumn(i)
        self.setIndentation(5)
        #self.setSortingEnabled(True)

        self.clicked.connect(
            getattr(self.parent, cfg["NAV_FUNCS"]["nav_clicked"]))

    def set_proj_path(self, path):
        if path is None:
            #TODO: Error Handling
            pass
        mem.set_img_path(path)
        self.setRootIndex(self.model.setRootPath(path))

class ImageViewer(QScrollArea):
    def __init__(self, parent = None):
        super(QScrollArea, self).__init__(parent)

        self._img_label = QLabel()
        self.setWidget(self._img_label)
        self.init_img_label()

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalScrollBar().valueChanged.connect(lambda idx: self.scrolling_temp(idx))

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

class Toolbar(QWidget):

    def __init__(self, parent=None, fxns=None):
        super(QWidget, self).__init__()
        self.parent = parent

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)

        self.init_buttons(fxns)
    
    def init_buttons(self, fxns):
        buttons = []

        s = self.parent.frameGeometry().height() * cfg["TBAR_ISIZE_REL"]
        m = s * cfg["TBAR_ISIZE_MARGIN"]

        for fxn in fxns:
            icon = QIcon()
            path = cfg["TBAR_IMG_ASSETS"] + fxn + ".png"
            if (exists(path)):
                icon = QIcon(path)
            else: icon = QIcon(cfg["TBAR_ICON_IMG"])
            
            buttons.append(QPushButton(self))
            buttons[-1].setIcon(icon)
            buttons[-1].setIconSize(QSize(s,s))
            buttons[-1].setFixedSize(QSize(m,m))
            buttons[-1].clicked.connect(getattr(self.parent, fxn))
            self.layout.addWidget(buttons[-1])

class Ribbon(QTabWidget):
    def __init__(self, parent=None):
        super(QTabWidget, self).__init__(parent) #remove parent?
        self.parent = parent
        h = self.parent.frameGeometry().height() * cfg["TBAR_ISIZE_REL"] * cfg["RBN_HEIGHT"]
        self.setFixedHeight(h)
        for tab_name, tools in cfg["TBAR_FUNCS"].items():
            self.addTab(Toolbar(parent=self.parent, fxns=tools), tab_name)

