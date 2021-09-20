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

        self.canvas = OCRCanvas(self, self.tracker)
        self.explorer = ImageNavigator(self, self.tracker)

        main_widget = QWidget()
        self.hlayout = QHBoxLayout(main_widget)
        self.hlayout.addWidget(self.explorer, cfg["NAV_VIEW_RATIO"][0])
        self.hlayout.addWidget(self.canvas, cfg["NAV_VIEW_RATIO"][1])

        # Ribbon is off by 2 pixels on my machine
        # Might need to check this on another pc
        self.hlayout.setContentsMargins(0,0,2,0)

        vlayout.addWidget(main_widget)        

    def view_image_from_explorer(self, filename): 
        self.tracker.p_image = filename
        if not self.tracker.p_image.is_valid():
            return False
        self.canvas.view_image()
        return True

    def open_dir(self):
        filepath = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            "." # , QFileDialog.DontUseNativeDialog
        )

        if filepath:
            # self.tracker.p_image = filename
            self.tracker.filepath = filepath
            self.explorer.set_directory(filepath)

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
        index = self.explorer.indexAbove(self.explorer.currentIndex())
        if (not index.isValid()):
            return
        self.explorer.setCurrentIndex(index)

    def load_next_image(self):
        # change gray to blue selection
        index = self.explorer.indexBelow(self.explorer.currentIndex())
        if (not index.isValid()):
            return
        self.explorer.setCurrentIndex(index)

    def load_image_at_idx(self):
        row_count = self.explorer.model.rowCount(self.explorer.rootIndex())
        i, _ = QInputDialog.getInt(
            self, 
            'Jump to', 
            f'Enter page number: (max is {row_count})',
            value = -1,
            min = 1,
            max = row_count)
        if (i == -1):
            return

        index = self.explorer.model.index(i-1, 0, self.explorer.rootIndex())
        self.explorer.setCurrentIndex(index)

    def toggle_manual_ocr(self):
        # should be on by default
        pass

    def toggle_auto_ocr(self):
        pass