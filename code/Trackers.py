from PyQt5.QtGui import QPixmap
from default import cfg
from os.path import isfile, join, splitext, normpath,abspath, split
from os import listdir

class Tracker:
    
    def __init__(self, filename=cfg["HOME_IMAGE"]):
        self._p_image = PImage(filename)
        self._p_mask = PImage()

        self._filepath = split(abspath(filename))[0]

        self._image_list = []

        self._mode = 0
    
    @property
    def p_image(self): 
        return self._p_image

    @p_image.setter
    def p_image(self, image):
        # TODO: use match case when 3.10 comes out
        if (type(image) is str):
            self._p_image = QPixmap(image)
            self._p_image.filename = image

    @property
    def p_mask(self):
        return self._p_mask
    
    @p_mask.setter
    def p_mask(self, image):
        self._p_mask = image

    @property
    def filepath(self):
        return self._filepath
    
    @filepath.setter
    def filepath(self, filepath):
        self._filepath = filepath
        filelist = filter(lambda f: isfile(join(self.filepath, 
                        f)), listdir(self.filepath))
        self._image_list = list(map(lambda p: normpath(join(self.filepath, p)),
                        filter((lambda f: ('*'+splitext(f)[1]) 
                            in cfg["IMAGE_EXTENSIONS"]), filelist)))

    def is_valid_image_idx(self, idx):
        return idx >= 0 and idx < len(self._image_list)


class PImage(QPixmap):
    
    def __init__(self, filename=None):
        super(QPixmap, self).__init__(filename)

        # Current directory + filename
        self._filename = filename
        # Current directory
        self._filepath = None

    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, filename):
        self._filename = filename
    
