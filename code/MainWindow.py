from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout,
                            QWidget, QFileDialog, QInputDialog)
from GUIElements import ImageNavigator, Ribbon, OCRCanvas
from default import cfg

class PMainWindow(QWidget):
    # TODO: add pyqtSlot decorator that will update
    # all GUI elements on the window

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__(parent)
        self.tracker = tracker

        vlayout = QVBoxLayout(self)

        self.ribbon = Ribbon(self, self.tracker)
        vlayout.addWidget(self.ribbon)

        self.explorer = ImageNavigator(self, self.tracker)
        self.canvas = OCRCanvas(self, self.tracker)

        main_widget = QWidget()
        self.hlayout = QHBoxLayout(main_widget)
        self.init_main_widget()

        vlayout.addWidget(main_widget)

    def init_main_widget(self):
        self.hlayout.addWidget(self.explorer, cfg["NAV_VIEW_RATIO"][0])
        self.hlayout.addWidget(self.canvas, cfg["NAV_VIEW_RATIO"][1])

        # Ribbon is off by 2 pixels on my machine
        # Might need to check this on another pc
        self.hlayout.setContentsMargins(0,0,2,0)

    def view_image_from_fdialog(self):
        idx_model = self.explorer.model.index(0, 0, self.explorer.rootIndex())
        filename = self.explorer.model.rootPath()+"/"+self.explorer.model.data(idx_model)
        self.tracker.p_image = filename

        # Sort items in tracker first then get the index of current image
        self.explorer.setCurrentIndex(self.explorer.model.index(0, 0, self.explorer.rootIndex()))

        if not self.tracker.p_image.is_valid():
            return False
        #self.tracker.p_image = filename
        self.canvas.view_image()
        return True

    def view_image_from_explorer(self, index):
        filename = self.explorer.model.fileInfo(index).absoluteFilePath()

        self.tracker.p_image = filename

        if not self.tracker.p_image.is_valid():
            return False

        self.canvas.view_image()
        return True

    def open_dir(self):
        # filename, _ = QFileDialog.getOpenFileName(
        #    self, 
        #    "Open Directory",
        #    ".",
        #    "Images (*.bmp *.gif *.jpg *.jpeg *.png *.pbm *.pgm *.ppm *.xbm *.xpm)")
        filepath = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            "." # , QFileDialog.DontUseNativeDialog
        )

        if filepath:
            # self.tracker.p_image = filename
            self.tracker.filepath = filepath
            self.explorer.set_proj_path(self.tracker.filepath)

    def save_image(self):
        print("Image saved to ", self.tracker.filepath)
        pass

    def delete_cache(self):
        print("Image deleted in ", self.tracker.filepath)
        pass

    def get_text_mask(self):
        print("Generating mask for ", self.tracker.filepath)
        pass

    def edit_text_mask(self):
        #TODO
        pass

    def save_current_mask(self):
        pass

    def delete_text_mask(self):
        print("Text deleted from mask ", self.tracker.filepath)
        pass

    def load_prev_image(self):
        # change gray to blue selection
        idx_model = self.explorer.indexAbove(self.explorer.currentIndex())
        if (not idx_model.isValid()):
            return
        self.explorer.setCurrentIndex(idx_model)
        self.view_image_from_explorer(idx_model)

    def load_next_image(self):
        # change gray to blue selection
        idx_model = self.explorer.indexBelow(self.explorer.currentIndex())
        if (not idx_model.isValid()):
            return
        self.explorer.setCurrentIndex(idx_model)
        self.view_image_from_explorer(idx_model)

    def load_image_at_idx(self):
        row_count = self.explorer.model.rowCount(self.explorer.rootIndex())
        idx, _ = QInputDialog.getInt(
            self, 
            'Jump to', 
            'Enter page number:',
            value = -1,
            min = 0,
            max = row_count-1)

        if (idx == -1):
            return

        # prev_idx = self.explorer.currentIndex()
        idx_model = self.explorer.model.index(idx, 0, self.explorer.rootIndex())
        
        self.explorer.setCurrentIndex(idx_model)
        self.view_image_from_explorer(idx_model)

        #self.explorer.setCurrentIndex(prev_idx)

    def toggle_manual_ocr(self):
        # should be on by default
        pass

    def toggle_auto_ocr(self):
        pass