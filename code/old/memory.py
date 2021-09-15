# TODO: Rewrite this as a Tracker object that will
# save image paths, pixmaps of original images and
# masks, button states, and window state
# Use decorators

class Tracker:
    pass

from default import cfg
from os import listdir
from os.path import isfile, join, splitext, normpath

img_index = 0
img_paths = []
mask_paths = []
curr_dir = cfg["NAV_ROOT"]
curr_img = cfg["HOME_IMAGE"]

def get_img_path():
    #global curr_dir
    return curr_dir

def set_img_path(path):
    global curr_dir, img_paths
    curr_dir = normpath(path)
    filelist = filter(lambda f: isfile(join(path, f)), listdir(path))
    img_paths = list(map(lambda p: normpath(join(path, p)),
                filter((lambda f: ('*'+splitext(f)[1]) in 
                        cfg["IMAGE_EXTENSIONS"]), filelist)))

def get_img_list():
    #global curr_dir
    return img_paths

def get_curr_img():
    #global curr_img
    return curr_img

def get_prev_img():
    pass

def set_curr_img(filepath):
    global curr_img
    curr_img = filepath

def set_prev_img():
    pass

def get_curr_mask():
    pass

def get_prev_mask():
    pass

def set_curr_mask():
    pass

def set_prev_mask():
    pass

def get_img_index():
    pass