"""
Poricom
Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from os.path import exists

from PyQt5.QtGui import (QIcon, QTransform)
from PyQt5.QtCore import (Qt, QDir, QSize, QRectF, QTimer, pyqtSlot)
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QApplication,
                            QWidget, QTabWidget, QPushButton, QComboBox,
                            QLabel, QTreeView, QFileSystemModel,
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

        self.setDirectory(tracker.filepath)
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

    def setDirectory(self, path):
        self.setRootIndex(self.model.setRootPath(path))
        self.setTopIndex()

class BaseCanvas(QGraphicsView):

    def __init__(self, parent=None, tracker=None):
        super(QGraphicsView, self).__init__(parent)
        self.parent = parent
        self.tracker = tracker

        self.timer_ = QTimer()
        self.timer_.setInterval(300)
        self.timer_.setSingleShot(True)
        self.timer_.timeout.connect(self.rubberBandStopped)

        self.canvasText = QLabel("", self, Qt.WindowStaysOnTopHint)
        self.canvasText.hide()
        self.canvasText.setObjectName("canvasText")

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(self.tracker.p_image.scaledToWidth(
            self.viewport().geometry().width(), Qt.SmoothTransformation))
        
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mouseMoveEvent(self, event):
        # TODO: There is rare bug where if the rubber band is moved too 
        # fast and is released near the point where the mouse is pressed,
        # PIL.UnidentifiedImageError occurs because the size of the image
        # is 0 bytes.
        rubberBandVisible = not self.rubberBandRect().isNull()
        if (event.buttons() & Qt.LeftButton) and rubberBandVisible:
            self.timer_.start()
        QGraphicsView.mouseMoveEvent(self, event)
    
    def mouseReleaseEvent(self, event):
        self.canvasText.hide()
        super().mouseReleaseEvent(event)

    @pyqtSlot()
    def rubberBandStopped(self):

        # use threading either here or on image_io
        if (self.canvasText.isHidden()):
            self.canvasText.show()

        lang = self.tracker.language + self.tracker.orientation
        log_path = self.tracker.filepath + "/log.txt"
        log_to_file = self.tracker.write_mode

        pixbox = self.grab(self.rubberBandRect())
        text = io_.pixboxToText(pixbox, lang, 
            self.tracker.ocr_model)
        io_.logText(text, mode=log_to_file, path=log_path)

        self.canvasText.setText(text)
        self.canvasText.adjustSize()

class FullScreen(BaseCanvas):

    def __init__(self, parent=None, tracker=None):
        super().__init__(parent, tracker)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def takeScreenshot(self):
        screen = QApplication.primaryScreen()
        s = screen.size()
        self.pixmap.setPixmap(
            screen.grabWindow(0).scaled(s.width(), s.height()))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def mouseReleaseEvent(self, event):
        self.parent.close()

class OCRCanvas(BaseCanvas):

    def __init__(self, parent=None, tracker=None):
        super().__init__(parent, tracker)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._zoomPanMode = False
        self.currentScale = 1

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(self.tracker.p_image.scaledToWidth(
            0.96*self.viewport().geometry().width(), Qt.SmoothTransformation))

    def viewImage(self):

        self.verticalScrollBar().setSliderPosition(0)
        self.pixmap.setPixmap(self.tracker.p_image.scaledToWidth(
            0.96*self.viewport().geometry().width(), Qt.SmoothTransformation))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def zoomView(self, isZoomIn, usingButton=False):
        factor = 1.1
        if usingButton:
            factor = 1.4

        if isZoomIn and self.currentScale < 15:
            self.scale(factor, factor)
            self.currentScale *= factor
        elif not isZoomIn and self.currentScale > 0.5:
            self.scale(1/factor, 1/factor)
            self.currentScale /= factor

    def toggleZoomPanMode(self):
        self._zoomPanMode = not self._zoomPanMode

    def resizeEvent(self, event):
        self.viewImage()
        QGraphicsView.resizeEvent(self, event)

    def wheelEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        zoomMode = pressedKey == Qt.ControlModifier or self._zoomPanMode

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if zoomMode:
            if event.angleDelta().y() > 0:
                isZoomIn = True
            elif event.angleDelta().y() < 0:
                isZoomIn = False
            self.zoomView(isZoomIn)

        if not zoomMode:
            QGraphicsView.wheelEvent(self, event)

    def mouseMoveEvent(self, event):
        pressedKey = QApplication.keyboardModifiers()
        panMode = pressedKey == Qt.ControlModifier or self._zoomPanMode

        if panMode:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.RubberBandDrag)

        BaseCanvas.mouseMoveEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        self.setTransform(QTransform())
        self.currentScale = 1
        QGraphicsView.mouseDoubleClickEvent(self, event)

class RibbonTab(QWidget):

    def __init__(self, parent=None, funcs=None, 
        tracker=None, tab_name=""):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker
        self.isSettingsTab = tab_name == "SETTINGS"

        self.button_list = []
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)

        self.initButtons(funcs)

    def initButtons(self, funcs):

        for func_name, func_cfg in funcs.items():
            self.loadButtonConfig(func_name, func_cfg)
            self.layout.addWidget(self.button_list[-1],
                alignment=getattr(Qt, func_cfg["align"]))
        self.layout.addStretch()

        if self.isSettingsTab:
            self.layout.addWidget(LanguagePicker(self.parent, self.tracker))
        self.layout.addWidget(PageNavigator(self.parent))

    def loadButtonConfig(self, b_name, b_config):

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

        tooltip = f"<h3 style='margin-bottom: 4px;'>{b_config['help_title']}\
            </h3><p style='margin-top: 0;'>{b_config['help_msg']}</p>"
        self.button_list[-1].setToolTip(tooltip)
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
            self.loadButtonConfig(func_name, func_cfg)

        self.layout.addWidget(self.button_list[0], 0, 0, 1, 1)
        self.layout.addWidget(self.button_list[1], 1, 0, 1, 1)
        self.layout.addWidget(self.button_list[2], 0, 1, 1, 2)
        self.layout.addWidget(self.button_list[3], 1, 1, 1, 1)
        self.layout.addWidget(self.button_list[4], 1, 2, 1, 1)

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
        self.language.currentIndexChanged.connect(self.changeLanguage)

        self.orientation = QComboBox()
        self.orientation.addItems(cfg["ORIENTATION"])
        self.layout.addWidget(self.orientation, 1, 0)
        self.orientation.currentIndexChanged.connect(self.changeOrientation)

    def changeLanguage(self, i):
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

    def changeOrientation(self, i):
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
                    tracker=self.tracker, tab_name=tab_name), tab_name)

