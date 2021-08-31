from PyQt5.QtCore import Qt, QDir, pyqtSignal, pyqtSlot
from PyQt5.QtGui import (QImage, QPixmap)
from PyQt5.QtWidgets import (QLabel, QScrollArea, QSizePolicy)
from PyQt5.QtWidgets import (QWidget, QFileSystemModel, QTreeView,
                            QHBoxLayout)

import memory as mem
from default import cfg

class ImageNavigator(QWidget):

    some_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        _layout = QHBoxLayout(self)
        _layout.setContentsMargins(0,0,2,0)

        self.model = QFileSystemModel()
        self.init_fs_model()

        self.treeview = QTreeView()
        self.treeview.setModel(self.model)
        self.init_treeview()
        _layout.addWidget(self.treeview, cfg["NAV_VIEW_RATIO"][0])

        self.image_viewer = ImageViewer()
        _layout.addWidget(self.image_viewer, cfg["NAV_VIEW_RATIO"][1])

        self.mask_viewer = ImageViewer()
        _layout.addWidget(self.mask_viewer, cfg["NAV_VIEW_RATIO"][1])
        self.mask_viewer.setHidden(True)

        self.set_proj_path(mem.get_img_path())

    def init_fs_model(self):
        self.model.setFilter(QDir.Files)
        self.model.setNameFilterDisables(False)
        self.model.setNameFilters(cfg["IMAGE_EXTENSIONS"])

        self.model.directoryLoaded.connect(self.load_default_img)
        #self.model.rootPathChanged.connect(self.set_proj_path)

    def init_treeview(self):
        for i in range(1,4):
            self.treeview.hideColumn(i)
        self.treeview.setIndentation(5)

        self.treeview.clicked.connect(self.view_image_from_explorer)

    def view_image_from_explorer(self, index):
        fp = self.model.fileInfo(index).absoluteFilePath()
        mem.set_curr_img(fp)
        self.image_viewer.view_image()
    
    def view_image_from_toolbar(self, mode=0):
        fp = mem.get_curr_img()
        mem.set_curr_img(fp)
        self.image_viewer.view_image()
        pass
    
    def set_proj_path(self, path):
        if path is None:
            #TODO: Error Handling
            pass
        mem.set_img_path(path)
        self.treeview.setRootIndex(self.model.setRootPath(path))

    def load_default_img(self):
        fp = self.model.index(0, 0, self.model.index(self.model.rootPath()))
        mem.set_curr_img(self.model.rootPath()+"/"+self.model.data(fp))
        self.image_viewer.view_image()
    


class ImageViewer(QScrollArea):
    def __init__(self, parent = None):
        super(QScrollArea, self).__init__(parent)

        self._img_label = QLabel()
        self.setWidget(self._img_label)
        self.init_img_label()

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.verticalScrollBar().valueChanged.connect(lambda idx: self.kekw(idx))

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
    
    def kekw(self,idx):
        print(idx)