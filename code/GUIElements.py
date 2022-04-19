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
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QVBoxLayout,
                            QApplication, QTreeView, QFileSystemModel,
                            QWidget, QTabWidget, QPushButton,
                            QComboBox, QDialog, QDialogButtonBox,
                            QGraphicsView, QGraphicsScene, QLabel)

import image_io as io_
from utils.config import cfg
from utils.editor import editConfig, editCBoxConfig, editPreviewStyle

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
        nextIndex = self.indexBelow(current)
        filenext = self.model.fileInfo(nextIndex).absoluteFilePath()
        self.parent.view_image_from_explorer(filename, filenext)
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
        log_path = self.tracker.filepath + "/log.txt"
        log_to_file = self.tracker.write_mode
        text = self.canvasText.text()
        io_.logText(text, mode=log_to_file, path=log_path)
        self.canvasText.hide()
        super().mouseReleaseEvent(event)

    @pyqtSlot()
    def rubberBandStopped(self):

        # use threading either here or on image_io
        if (self.canvasText.isHidden()):
            self.canvasText.show()

        lang = self.tracker.language + self.tracker.orientation
        pixbox = self.grab(self.rubberBandRect())
        text = io_.pixboxToText(pixbox, lang, 
            self.tracker.ocr_model)

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
        BaseCanvas.mouseReleaseEvent(self, event)
        self.parent.close()

class OCRCanvas(BaseCanvas):

    def __init__(self, parent=None, tracker=None):
        super().__init__(parent, tracker)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self._viewImageMode = cfg["VIEW_IMAGE_MODE"]
        self._splitViewMode = cfg["SPLIT_VIEW_MODE"]
        self._zoomPanMode = False
        self.currentScale = 1
        self._scrollAtMin = 0
        self._scrollAtMax = 0

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pixmap = self.scene.addPixmap(self.tracker.p_image.scaledToWidth(
            self.viewport().geometry().width(), Qt.SmoothTransformation))

    def viewImage(self):
        self.verticalScrollBar().setSliderPosition(0)
        if self._viewImageMode == 0:
            self.pixmap.setPixmap(self.tracker.p_image.scaledToWidth(
                self.viewport().geometry().width(), Qt.SmoothTransformation))
        elif self._viewImageMode == 1:
            self.pixmap.setPixmap(self.tracker.p_image.scaledToHeight(
                self.viewport().geometry().height(), Qt.SmoothTransformation))
        elif self._viewImageMode == 2:
            self.pixmap.setPixmap(self.tracker.p_image.scaled(
                self.viewport().geometry().width(), self.viewport().geometry().height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.scene.setSceneRect(QRectF(self.pixmap.pixmap().rect()))

    def setViewImageMode(self, mode):
        self._viewImageMode = mode
        editConfig("VIEW_IMAGE_MODE", mode)
        self.viewImage()

    def splitViewMode(self):
        return self._splitViewMode
    
    def toggleSplitView(self):
        self._splitViewMode = not self._splitViewMode
        editConfig("SPLIT_VIEW_MODE", self._splitViewMode)

    def zoomView(self, isZoomIn, usingButton=False):
        factor = 1.1
        if usingButton:
            factor = 1.4

        if isZoomIn and self.currentScale < 15:
            self.scale(factor, factor)
            self.currentScale *= factor
        elif not isZoomIn and self.currentScale > 0.35:
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
            if (event.angleDelta().y() < 0 and
                self.verticalScrollBar().value() == self.verticalScrollBar().maximum()):
                if (self._scrollAtMax == 3):
                    self.parent.load_next_image()
                    self._scrollAtMax = 0
                    return
                else:
                    self._scrollAtMax += 1

            if (event.angleDelta().y() > 0 and
                self.verticalScrollBar().value() == self.verticalScrollBar().minimum()):
                if (self._scrollAtMin == 3):
                    self.parent.load_prev_image()
                    self._scrollAtMin = 0
                    return
                else:
                    self._scrollAtMin += 1
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
        self.tab_name = tab_name

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

        if hasattr(self.parent, b_name):
            self.button_list[-1].clicked.connect(getattr(self.parent, b_name))
        else:
            self.button_list[-1].clicked.connect(getattr(self.parent, 'poricomNoop'))

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

class BasePicker(QWidget):
    def __init__(self, parent, tracker, list_top, list_bot):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.picktop = QComboBox()
        self.picktop.addItems(list_top)
        self.layout.addWidget(self.picktop, 0, 1)
        self.nametop = QLabel("")
        self.layout.addWidget(self.nametop, 0, 0)
        if list_bot:
            self.pickbot = QComboBox()
            self.pickbot.addItems(list_bot)
            self.layout.addWidget(self.pickbot, 1, 1)
            self.namebot = QLabel("")
            self.layout.addWidget(self.namebot, 1, 0)

class LanguagePicker(BasePicker):
    def __init__(self, parent, tracker, 
        list_top=cfg["LANGUAGE"], list_bot=cfg["ORIENTATION"]):

        super().__init__(parent, tracker, list_top, list_bot)
        self.picktop.currentIndexChanged.connect(self.changeLanguage)
        self.picktop.setCurrentIndex(cfg["SELECTED_INDEX"]["language"])
        self.nametop.setText("Language: ")
        self.pickbot.currentIndexChanged.connect(self.changeOrientation)
        self.pickbot.setCurrentIndex(cfg["SELECTED_INDEX"]["orientation"])
        self.namebot.setText("Orientation: ")

        self.language_index = self.picktop.currentIndex()
        self.orientation_index = self.pickbot.currentIndex()

    def changeLanguage(self, i):
        self.language_index = i
        selected_language = self.picktop.currentText().strip()
        if selected_language == "Japanese":
            self.tracker.language = "jpn"
        if selected_language == "Korean":
            self.tracker.language = "kor"
        if selected_language == "Chinese SIM":
            self.tracker.language = "chi_sim"
        if selected_language == "Chinese TRA":
            self.tracker.language = "chi_tra"
        if selected_language == "English":
            self.tracker.language = "eng"

    def changeOrientation(self, i):
        self.orientation_index = i
        selected_orientation = self.pickbot.currentText().strip()
        if selected_orientation == "Vertical":
            self.tracker.orientation = "_vert"
        if selected_orientation == "Horizontal":
            self.tracker.orientation = ""

    def applyChanges(self):
        editCBoxConfig(self.language_index, 'language')
        editCBoxConfig(self.orientation_index, 'orientation')
        cfg["SELECTED_INDEX"]["language"] = self.language_index
        cfg["SELECTED_INDEX"]["orientation"] = self.orientation_index

class FontPicker(BasePicker):
    def __init__(self, parent, tracker,
        list_top=cfg["FONT_STYLE"], list_bot=cfg["FONT_SIZE"]):
        super().__init__(parent, tracker, list_top, list_bot)
        self.picktop.currentIndexChanged.connect(self.changeFontStyle)
        self.picktop.setCurrentIndex(cfg["SELECTED_INDEX"]["font_style"])
        self.nametop.setText("Font Style: ")
        self.pickbot.currentIndexChanged.connect(self.changeFontSize)
        self.pickbot.setCurrentIndex(cfg["SELECTED_INDEX"]["font_size"])
        self.namebot.setText("Font Size: ")

        self.font_style_text = "  font-family: 'Poppins';\n"
        self.font_size_text = "  font-size: 16pt;\n"
        self.font_style_index = self.picktop.currentIndex()
        self.font_size_index = self.pickbot.currentIndex()

    def changeFontStyle(self, i):
        self.font_style_index = i
        selected_font_style = self.picktop.currentText().strip()
        replacement_text = f"  font-family: '{selected_font_style}';\n"
        self.font_style_text = replacement_text

    def changeFontSize(self, i):
        self.font_size_index = i
        selected_font_size = int(self.pickbot.currentText().strip())
        replacement_text = f"  font-size: {selected_font_size}pt;\n"
        self.font_size_text = replacement_text

    def applyChanges(self):
        editCBoxConfig(self.font_style_index, 'font_style')
        editCBoxConfig(self.font_size_index, 'font_size')
        cfg["SELECTED_INDEX"]["font_style"] = self.font_style_index
        cfg["SELECTED_INDEX"]["font_size"] = self.font_size_index
        editPreviewStyle(41, self.font_style_text)
        editPreviewStyle(42, self.font_size_text)

class ScaleImagePicker(BasePicker):
    def __init__(self, parent, tracker, 
        list_top=cfg["IMAGE_SCALING"], list_bot=[]):

        super().__init__(parent, tracker, list_top, list_bot)
        self.picktop.currentIndexChanged.connect(self.changeScaling)
        self.picktop.setCurrentIndex(cfg["SELECTED_INDEX"]["image_scaling"])
        self.nametop.setText("Image Scaling: ")

        self.scaling_index = self.picktop.currentIndex()

    def changeScaling(self, i):
        self.scaling_index = i

    def applyChanges(self):
        self.parent.canvas.setViewImageMode(self.scaling_index)
        editCBoxConfig(self.scaling_index, 'image_scaling')
        cfg["SELECTED_INDEX"]["image_scaling"] = self.scaling_index

class PickerPopup(QDialog):
    def __init__(self, widget):
        super(QDialog, self).__init__(None, 
            Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.widget = widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(widget)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout().addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.okClickedEvent)
        self.buttonBox.rejected.connect(self.cancelClickedEvent)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)        
    
    def okClickedEvent(self):
        self.widget.applyChanges()
        self.close()
    
    def cancelClickedEvent(self):
        self.close()

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

