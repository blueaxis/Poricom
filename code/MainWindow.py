from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout,
                            QWidget, QFileDialog)

from GUIElements import ImageNavigator, ImageViewer, Ribbon, Canvas
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
        #self.viewer = ImageViewer()
        self.canvas = Canvas(self, self.tracker)

        main_widget = QWidget()
        self.hlayout = QHBoxLayout(main_widget)
        self.init_main_widget()

        vlayout.addWidget(main_widget)

    def init_main_widget(self):
        self.hlayout.addWidget(self.explorer, cfg["NAV_VIEW_RATIO"][0])
        #self.hlayout.addWidget(self.viewer, cfg["NAV_VIEW_RATIO"][1])
        self.hlayout.addWidget(self.canvas, cfg["NAV_VIEW_RATIO"][1])

        self.hlayout.setContentsMargins(0,0,2,0)

    def load_default_img(self):
        model_idx = self.explorer.model.index(0, 0, 
            self.explorer.model.index(self.explorer.model.rootPath()))
        filename = self.explorer.model.rootPath()+"/"+self.explorer.model.data(model_idx)

        self.tracker.p_image = filename
        #self.viewer.view_image()
        self.canvas.view_image()

    def view_image_from_explorer(self, index):
        filename = self.explorer.model.fileInfo(index).absoluteFilePath()

        self.tracker.p_image = filename
        #self.viewer.view_image()
        self.canvas.view_image()

    def update_window(self, mode=0):
        self.explorer.set_proj_path(self.tracker.filepath)

    def open_dir(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if path:
            self.tracker.filepath = path
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
        idx_int = self.explorer.currentIndex().row() - 1
        idx_model = self.explorer.model.index(idx_int, 0, self.explorer.rootIndex())
        self.explorer.setCurrentIndex(idx_model)
        self.view_image_from_explorer(idx_model)

    def load_next_image(self):
        # change gray to blue selection
        idx_int = self.explorer.currentIndex().row() + 1
        idx_model = self.explorer.model.index(idx_int, 0, self.explorer.rootIndex())
        self.explorer.setCurrentIndex(idx_model)
        self.view_image_from_explorer(idx_model)

    def load_image_at_idx(self, idx_int):
        idx_model = self.explorer.model.index(idx_int, 0, self.explorer.rootIndex())
        self.explorer.setCurrentIndex(idx_model)
        self.view_image_from_explorer(idx_model)

    def toggle_manual_ocr(self):
        pass

    def toggle_auto_ocr(self):
        pass