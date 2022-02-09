from os.path import exists

from PyQt5.QtCore import Qt, QDir, QSize, QRectF, QPoint, QRect, QTimer
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QRubberBand, QWidget,
                            QPushButton, QTabWidget, QComboBox,
                            QTreeView, QFileSystemModel,
                            QGraphicsView, QGraphicsScene)

import image_io as io_
from default import cfg

# TODO: Decorate slots using pyqtSlot

class ImageNavigator(QTreeView):
    layoutCheck = False
    def __init__(self, parent=None, tracker=None):
        super(QTreeView, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.model = QFileSystemModel()
        self.model.setFilter(QDir.Files)
        self.model.setNameFilterDisables(False)
        self.model.setNameFilters(cfg["IMAGE_EXTENSIONS"])
        self.setModel(self.model)

        for i in range(1,4):
            self.hideColumn(i)
        self.setIndentation(0)

        self.set_directory(tracker.filepath)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def currentChanged(self, current, previous):
        if not current.isValid():
            current = self.model.index(0, 0, self.rootIndex())
        filename = self.model.fileInfo(current).absoluteFilePath()
        self.parent.view_image_from_explorer(filename)
        QTreeView.currentChanged(self, current, previous)
    
    def setTopIndex(self):
        topIndex = self.model.index(0, 0, self.rootIndex())
        if topIndex.isValid():
            self.setCurrentIndex(topIndex)
            if self.layoutCheck:
                self.model.layoutChanged.disconnect(self.setTopIndex)
                self.layoutCheck = False
        else:
            if not self.layoutCheck:
                self.model.layoutChanged.connect(self.setTopIndex)
                self.layoutCheck = True

    def set_directory(self, path):
        self.setRootIndex(self.model.setRootPath(path))
        self.setTopIndex()

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
        self.timer_.setInterval(300)
        self.timer_.setSingleShot(True)
        self.timer_.timeout.connect(self.rubberBandStopped)

        self.canvasText = QLabel("", self, Qt.WindowStaysOnTopHint)
        self.canvasText.hide()
        self.canvasText.setObjectName("canvasText")

    def view_image(self):       

        self.verticalScrollBar().setSliderPosition(0)
        self.pixmap.setPixmap(self.tracker.p_image.scaledToWidth(
            0.96*self.viewport().geometry().width(), Qt.SmoothTransformation))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def resizeEvent(self, event):
        self.view_image()
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

            self.canvasText.hide()
            # self.r_band.close()
        
        QGraphicsView.mouseReleaseEvent(self, event)
    
    def mouseMoveEvent(self, event):
        if ((event.buttons() & Qt.LeftButton)):
            self.timer_.start()
            self.r_band.setGeometry(QRect(self.last_point, event.pos()).normalized())
        QGraphicsView.mouseMoveEvent(self, event)

    def rubberBandStopped(self):

        # use threading either here or on image_io
        if (self.canvasText.isHidden()):
            self.canvasText.show()

        lang = self.tracker.language + self.tracker.orientation
        log_path = self.tracker.filepath + "/log.txt"
        log_to_file = self.tracker.write_mode

        text = io_.pixbox_to_text(self.grab(self.r_band.geometry()), lang, 
            self.tracker.ocr_model)
        io_.log_text(text, mode=log_to_file, path=log_path)

        self.canvasText.setText(text)
        self.canvasText.adjustSize()

class RibbonTab(QWidget):

    def __init__(self, parent=None, funcs=None, tracker=None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.button_list = []
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)
        
        self.init_buttons(funcs)
    
    def init_buttons(self, funcs):

        for func_name, func_cfg in funcs.items():
            self.load_button_config(func_name, func_cfg)
            self.layout.addWidget(self.button_list[-1],
                alignment=getattr(Qt, func_cfg["align"]))
        self.layout.addStretch()

        self.layout.addWidget(LanguagePicker(self.parent, self.tracker))
        self.layout.addWidget(PageNavigator(self.parent))
    
    def load_button_config(self, b_name, b_config):

        w = self.parent.frameGeometry().height()*cfg["TBAR_ISIZE_REL"]*b_config["icon_w"]
        h = self.parent.frameGeometry().height()*cfg["TBAR_ISIZE_REL"]*b_config["icon_h"]
        m = cfg["TBAR_ISIZE_MARGIN"]

        icon = QIcon()
        path = cfg["TBAR_ICONS"] + b_config["path"]
        if (exists(path)):
            icon = QIcon(path)
        else: icon = QIcon(cfg["TBAR_ICON_DEFAULT"])

        #TODO: add keyboard shortcut using name scheme

        self.button_list.append(QPushButton(self))
        self.button_list[-1].setObjectName(b_name)

        self.button_list[-1].setIcon(icon)
        self.button_list[-1].setIconSize(QSize(w,h))
        self.button_list[-1].setFixedSize(QSize(w*m,h*m))

        self.button_list[-1].setToolTip(b_config["help_msg"])
        self.button_list[-1].setCheckable(b_config["toggle"])

        self.button_list[-1].clicked.connect(getattr(self.parent, b_name))

class PageNavigator(RibbonTab):

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
        self.layout.addWidget(self.button_list[1], 1, 0, 1, 1)
        self.layout.addWidget(self.button_list[2], 1, 1, 1, 1)

class LanguagePicker(QWidget):

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        self.language = QComboBox()
        self.language.addItems(cfg["LANGUAGE"])
        self.layout.addWidget(self.language, 0, 0)
        self.language.currentIndexChanged.connect(self.change_language)

        self.orientation = QComboBox()
        self.orientation.addItems(cfg["ORIENTATION"])
        self.layout.addWidget(self.orientation, 1, 0)
        self.orientation.currentIndexChanged.connect(self.change_orientation)
    
    def change_language(self, i):
        if self.language.currentText().strip() == "Japanese":
            self.tracker.language = "jpn"
        if self.language.currentText().strip() == "Korean":
            self.tracker.language = "kor"
        if self.language.currentText().strip() == "Chinese SIM":
            self.tracker.language = "chi_sim"
        if self.language.currentText().strip() == "Chinese TRA":
            self.tracker.language = "chi_tra"
        if self.language.currentText().strip() == "English":
            self.tracker.language = "eng"

    def change_orientation(self, i):
        if self.orientation.currentText().strip() == "Vertical":
            self.tracker.orientation = "_vert"
        if self.orientation.currentText().strip() == "Horizontal":
            self.tracker.orientation = ""

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

