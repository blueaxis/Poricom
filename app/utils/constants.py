 
from .types import ButtonConfigDict
from sys import platform

# ------------------------------------- General ------------------------------------- #

APP_NAME = "P-plot"
APP_LOGO = "./assets/images/icons/logo.ico"

IMAGE_EXTENSIONS = [
    "*.bmp",
    "*.gif",
    "*.jpeg",
    "*.jpg",
    "*.pbm",
    "*.pgm",
    "*.png",
    "*.ppm",
    "*.webp",
    "*.xbm",
    "*.xpm",
]

# Settings Popup Choices
TOGGLE_CHOICES = [" Desactivado", " Activado"]

OCR_MODEL = [" MangaOCR", " Tesseract"]
TRANSLATE_MODEL = [" ArgosTranslate", " ChatGPT", " DeepL"]
LANGUAGE = [" Japonés", " Coreano", " Chino SIMP", " Chino TRAD  ", " Inglés"]
ORIENTATION = [" Vertical", " Horizontal"]

IMAGE_SCALING = ["Ajustar al ancho", "Ajustar al alto", "Ajustar a la pantalla"]

FONT_SIZE = [" 12", " 14", " 16", " 20", " 24", " 32", " 40", " 56", " 72"]
FONT_STYLE = [" Helvetica", " Poppins", " Arial", " Verdana", " Times New Roman"]

MODIFIER = [
    " Ctrl",
    " Shift",
    " Alt",
    " Ctrl+Alt",
    " Shift+Alt",
    " Shift+Ctrl",
    " Shift+Alt+Ctrl",
    " Sin Modificador",
]

PLATFORM = platform

# Paths
STYLESHEET_LIGHT = "./assets/styles.qss"
STYLESHEET_DARK = "./assets/styles-dark.qss"

TESSERACT_LANGUAGES = "./assets/languages/"

TOOLBAR_ICONS = "./assets/images/icons/"
TOOLBAR_ICON_DEFAULT = "./assets/images/icons/default_icon.png"

EXPLORER_ROOT_DEFAULT = "./assets/images/"

PORICOM_CACHE = "/tmp/poricom_cache" if PLATFORM == "linux" else "./poricom_cache"

# Messages
LOAD_MODEL_MESSAGE = (
    "Si estás ejecutando esto por primera vez, se descargará el modelo MangaOCR, que"
    "tiene un tamaño aproximado de 400 MB, esto ayudará a mejorar la precisión de la"
    "detección de texto en japonés en Poricom. Si ya está en tu caché, tardará unos"
    "segundos en cargar el modelo."
)

# ------------------------------------ Settings ------------------------------------- #

SETTINGS_FILE_DEFAULT = "./bin/poricom-config.ini"

# Window
MAIN_WINDOW_DEFAULTS = {
    "usarOCRoffline": "false",
    "hasLoadModelPopup": "true",
    "logToFile": "true",
    "mangaOCRPath": "",
    "stylesheetPath": "./assets/styles.qss",
}
MAIN_WINDOW_TYPES = {
    "usarOCRoffline": bool,
    "hasLoadModelPopup": bool,
    "logToFile": bool,
}

# View
MAIN_VIEW_DEFAULTS = {"explorerPath": EXPLORER_ROOT_DEFAULT}
IMAGE_VIEW_DEFAULTS = {
    "viewImageMode": 0,
    "imageScalingIndex": 0,
    "splitViewMode": "false",
    "zoomPanMode": "false",
}
IMAGE_VIEW_TYPES = {"viewImageMode": int, "splitViewMode": bool, "zoomPanMode": bool}

# Tesseract
TESSERACT_DEFAULTS = {"language": "jpn", "orientation": "_vert"}

# Text Logging
TEXT_LOGGING_DEFAULTS = {"explorerPath": EXPLORER_ROOT_DEFAULT, "logToFile": "false"}
TEXT_LOGGING_TYPES = {"logToFile": bool}

# Translate
TRANSLATE_DEFAULTS = {"enableTranslate": "false"}
TRANSLATE_TYPES = {"enableTranslate": bool}

# --------------------------------------- UI ---------------------------------------- #

# Main view
MAIN_VIEW_RATIO = [3, 19, 4]

# Toolbar
TOOLBAR_ICON_SIZE = 0.05  # Fraction of primary screen height

NAVIGATION_FUNCTIONS: ButtonConfigDict = {
    "zoomIn": {
        "title": "Zoom in",
        "message": "Hint: Double click the image to reset zoom.",
        "path": "zoomIn.png",
        "toggle": False,
        "align": "AlignRight",
        "iconHeight": 0.45,
        "iconWidth": 0.45,
    },
    "zoomOut": {
        "title": "Zoom out",
        "message": "Hint: Double click the image to reset zoom.",
        "path": "zoomOut.png",
        "toggle": False,
        "align": "AlignRight",
        "iconHeight": 0.45,
        "iconWidth": 0.45,
    },
    "loadImageAtIndex": {
        "title": "",
        "message": "Jump to page",
        "path": "loadImageAtIndex.png",
        "toggle": False,
        "align": "AlignRight",
        "iconHeight": 0.45,
        "iconWidth": 1.3,
    },
    "loadPrevImage": {
        "title": "",
        "message": "Show previous image",
        "path": "loadPrevImage.png",
        "toggle": False,
        "align": "AlignRight",
        "iconHeight": 0.45,
        "iconWidth": 0.6,
    },
    "loadNextImage": {
        "title": "",
        "message": "Show next image",
        "path": "loadNextImage.png",
        "toggle": False,
        "align": "AlignRight",
        "iconHeight": 0.45,
        "iconWidth": 0.6,
    },
}
TOOLBAR_FUNCTIONS: dict[str, ButtonConfigDict] = {
    "archivo": {
        "openDir": {
            "title": "Abrir directorio de manga",
            "message": "Abre una carpeta que contenga el raw del manga.",
            "path": "openDir.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "openManga": {
            "title": "Abrir un archivo de manga",
            "message": "Que esté en estos formatos: cbr, cbz, pdf.",
            "path": "openManga.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "captureExternalHelper": {
            "title": "Capturar con screenshot",
            "message": "Esto minimizará la aplicación y ejecutará el OCR en la pantalla actual. También podrás usar el atajo ALT+Q (por default).",
            "path": "captureExternalHelper.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
    },
    "vista": {
        "toggleStylesheet": {
            "title": "Cambiar fondo",
            "message": "Cambia entre fondo oscuro y fondo claro.",
            "path": "toggleStylesheet.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "hideExplorer": {
            "title": "Esconder navegador",
            "message": "Minimiza el navegador de páginas y directorios.",
            "path": "hideExplorer.png",
            "toggle": True,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "modifyFontSettings": {
            "title": "Modificar fuente",
            "message": "Cambiar el estilo de fuente y el tamaño de fuente del texto de vista previa.",
            "path": "modifyFontSettings.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "toggleSplitView": {
            "title": "Activar vista dividida",
            "message": "Ver dos imágenes a la vez.",
            "path": "toggleSplitView.png",
            "toggle": True,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "modifyImageScaling": {
            "title": "Ajustar la escala",
            "message": "Ajusta la imagen según las opciones disponibles: ajustar al ancho, ajustar al alto, ajustar a la pantalla.",
            "path": "modifyImageScaling.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
    },
    "controles": {
        "toggleMouseMode": {
            "title": "Cambiar uso del ratón",
            "message": "Esto deshabilitará la detección de texto. Activa esto si no quieres mantener presionado CTRL para hacer zoom y desplazarte en la imagen.",
            "path": "toggleMouseMode.png",
            "toggle": True,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "modifyHotkeys": {
            "title": "Cambiar atajo de teclado",
            "message": "Cambia la combinación de teclas para captura de OCR.",
            "path": "modifyHotkeys.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
    },
    "detección": {
        "loadModel": {
            "title": "Cargar modelo de OCR",
            "message": "Administrar la configuración del modelo de detección.",
            "path": "loadModel.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "loadTranslateModel": {
            "title": "Cargar modelo de traducción",
            "message": "Administrar la configuración del modelo de traducción y las claves API.",
            "path": "loadTranslateModel.png",
            "toggle": False,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
        "toggleLogging": {
            "title": "Activar guardado de texto",
            "message": "Guardar el texto detectado en un archivo de texto ubicado en el directorio del proyecto actual.",
            "path": "toggleLogging.png",
            "toggle": True,
            "align": "AlignLeft",
            "iconHeight": 1.0,
            "iconWidth": 1.0,
        },
    },
}
