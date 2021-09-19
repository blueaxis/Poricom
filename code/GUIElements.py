from PyQt5.QtCore import Qt, QDir, QSize, QRectF, QPoint, QRect, QTimer
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QRubberBand, QWidget,
                            QPushButton, QTabWidget,
                            QTreeView, QFileSystemModel,
                            QGraphicsView, QGraphicsScene)

from os.path import exists
import image_io as io_
from default import cfg

# TODO: Decorate slots using pyqtSlot

class ImageNavigator(QTreeView):

    def __init__(self, parent=None, tracker=None):
        super(QTreeView, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.model = QFileSystemModel()
        self.init_fs_model()

        self.setModel(self.model)
        self.init_treeview()

        self.set_proj_path(tracker.filepath)

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
        self.tracker.filepath = path

        self.setRootIndex(self.model.setRootPath(path))

# TODO: Create an BaseCanvas class where 
# OCRCanvas and EditCanvas will inherit from.

class OCRCanvas(QGraphicsView):

    def __init__(self, parent=None, tracker=None):
        super(QGraphicsView, self).__init__(parent)
        self.parent = parent
        self.tracker = tracker

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.pixmap = self.scene.addPixmap(self.tracker.p_image.scaledToWidth(
            self.viewport().geometry().width()-100, Qt.SmoothTransformation))

        self.last_point = QPoint()
        self.r_band = QRubberBand(QRubberBand.Rectangle, self)
        
        self.timer_ = QTimer()
        self.timer_.setInterval(300);
        self.timer_.setSingleShot(True);
        self.timer_.timeout.connect(self.movement_end)
    
    def view_image(self):       

        self.verticalScrollBar().setSliderPosition(0)
        self.pixmap.setPixmap(self.tracker.p_image.scaledToWidth(
            self.viewport().geometry().width()-100, Qt.SmoothTransformation))

    def resizeEvent(self, event):
        self.view_image()
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))
        QGraphicsView.resizeEvent(self, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.r_band.setGeometry(QRect(self.last_point, QSize()))
            self.r_band.show()
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.r_band.setGeometry(QRect(self.last_point, event.pos()).normalized())
            self.r_band.hide()

            # use threading either here or on image_io
            io_.pixmap_to_text(self.grab(self.r_band.geometry()))
            # self.r_band.close()
        
        QGraphicsView.mouseReleaseEvent(self, event)
    
    def mouseMoveEvent(self, event):
        if ((event.buttons() & Qt.LeftButton)):
            self.timer_.start()
            self.r_band.setGeometry(QRect(self.last_point, event.pos()).normalized())
            # allow dynamic OCR while rectangle is being created
        QGraphicsView.mouseMoveEvent(self, event)

    def movement_end(self):
        print("Movement ended")
        # self.timer_.stop()

class PageNavigator(QWidget):

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker
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

class RibbonTab(QWidget):

    def __init__(self, parent=None, funcs=None, tracker=None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)
        self.button_list = []

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
    def __init__(self, parent=None, tracker=None):
        super(QTabWidget, self).__init__(parent) #remove parent?
        self.parent = parent
        self.tracker = tracker

        h = self.parent.frameGeometry().height() * \
            cfg["TBAR_ISIZE_REL"] * cfg["RBN_HEIGHT"]
        self.setFixedHeight(h)
        #TODO: add keyboard shortcut using name scheme
        for tab_name, tools in cfg["TBAR_FUNCS"].items():
            self.addTab(RibbonTab(parent=self.parent, funcs=tools,
                        tracker=self.tracker), tab_name)

