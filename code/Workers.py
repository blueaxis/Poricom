from PyQt5.QtCore import (QRunnable, QObject, 
                         pyqtSignal, pyqtSlot)

class BaseWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(BaseWorker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()
    @pyqtSlot()
    def run(self):
        output = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(output)
        self.signals.finished.emit()

class WorkerSignal(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)