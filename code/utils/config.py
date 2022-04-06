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

stylesheet_path = './assets/styles.qss'
cfg = {
    "IMAGE_EXTENSIONS": ["*.bmp", "*.gif", "*.jpg", "*.jpeg", "*.png", 
                         "*.pbm", "*.pgm", "*.ppm", "*.webp", "*.xbm", "*.xpm"],

    "LANGUAGE": [" Japanese", " Korean", " Chinese SIM", " Chinese TRA  ", " English"],
    "ORIENTATION": [" Vertical", " Horizontal"],
    "LANG_PATH": "./assets/languages/",

    "STYLES_PATH": "./assets/",
    "STYLES_DEFAULT": stylesheet_path,
    
    "NAV_VIEW_RATIO": [3,11],
    "NAV_ROOT": "./assets/images/",

    "NAV_FUNCS": {
        "path_changed": "view_image_from_fdialog",
        "nav_clicked": "view_image_from_explorer"
    },

    "LOGO": "./assets/images/icons/logo.ico",
    "HOME_IMAGE": "./assets/images/home.png",

    "RBN_HEIGHT": 2.4,

    "TBAR_ISIZE_REL": 0.1,
    "TBAR_ISIZE_MARGIN": 1.3,

    "TBAR_ICONS": "./assets/images/icons/",
    "TBAR_ICONS_LIGHT": "./assets/images/icons/",
    "TBAR_ICON_DEFAULT": "./assets/images/icons/default_icon.png",

    "TBAR_FUNCS": {
        "FILE": {
            "open_dir": {
                "help_title": "Open manga directory",
                "help_msg": "Open a directory containing images.",
                "path": "open_dir.png",
                "toggle": False,
                "align": "AlignLeft",
                "icon_h": 1.0,
                "icon_w": 1.0
            },
            "open_manga": {
                "help_title": "Open manga file",
                "help_msg": "Supports the following formats: cbr, cbz, pdf.",
                "path": "open_manga.png",
                "toggle": False,
                "align": "AlignLeft",
                "icon_h": 1.0,
                "icon_w": 1.0
            }
        },
        "SETTINGS": {
            "load_model": {
                "help_title": "Switch detection model",
                "help_msg": "Switch between MangaOCR and Tesseract models.",
                "path": "load_model.png",
                "toggle": True,
                "align": "AlignLeft",
                "icon_h": 1.0,
                "icon_w": 1.0
            },
            "toggle_logging": {
                "help_title": "Enable text logging",
                "help_msg": "Save detected text to a text file located in the \
                    current project directory.",
                "path": "toggle_logging.png",
                "toggle": True,
                "align": "AlignLeft",
                "icon_h": 1.0,
                "icon_w": 1.0
            },
            "toggle_mouse_mode": {
                "help_title": "Change mouse behavior",
                "help_msg": "This will disable text detection. Turn this on \
                    only if do not want to hold CTRL key to zoom and pan \
                    on an image.",
                "path": "toggle_mouse_mode.png",
                "toggle": True,
                "align": "AlignLeft",
                "icon_h": 1.0,
                "icon_w": 1.0
            },
            "toggle_stylesheet": {
                "help_title": "Change theme",
                "help_msg": "Switch between light and dark mode.",
                "path": "toggle_stylesheet.png",
                "toggle": False,
                "align": "AlignLeft",
                "icon_h": 1.0,
                "icon_w": 1.0
            }
        }
    },

    "MODE_FUNCS": {
        "zoom_in": {
            "help_title": "Zoom in",
            "help_msg": "Hint: Double click the image to reset zoom.",
            "path": "zoom_in.png",
            "toggle": False,
            "align": "AlignRight",
            "icon_h": 0.45,
            "icon_w": 0.45
        },
        "zoom_out": {
            "help_title": "Zoom out",
            "help_msg": "Hint: Double click the image to reset zoom.",
            "path": "zoom_out.png",
            "toggle": False,
            "align": "AlignRight",
            "icon_h": 0.45,
            "icon_w": 0.45
        },
        "load_image_at_idx": {
            "help_title": "",
            "help_msg": "Jump to page",
            "path": "load_image_at_idx.png",
            "toggle": False,
            "align": "AlignRight",
            "icon_h": 0.45,
            "icon_w": 1.3
        },
        "load_prev_image": {
            "help_title": "",
            "help_msg": "Show previous image",
            "path": "load_prev_image.png",
            "toggle": False,
            "align": "AlignRight",
            "icon_h": 0.45,
            "icon_w": 0.6
        },
        "load_next_image": {
            "help_title": "",
            "help_msg": "Show next image",
            "path": "load_next_image.png",
            "toggle": False,
            "align": "AlignRight",
            "icon_h": 0.45,
            "icon_w": 0.6
        }
    }
}