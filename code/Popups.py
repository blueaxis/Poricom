"""
Poricom Popup Components

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

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QGridLayout, QVBoxLayout, QWidget, 
                            QLabel, QLineEdit, QComboBox, 
                            QDialog, QDialogButtonBox, QMessageBox)

from utils.config import (editSelectionConfig, editStylesheet)

class MessagePopup(QMessageBox):
    def __init__(self, title, message, flags = QMessageBox.Ok):
        super(QMessageBox, self).__init__(QMessageBox.NoIcon, 
                                          title,
                                          message,
                                          flags)

class BasePicker(QWidget):
    def __init__(self, parent, tracker, optionLists=[]):
        super(QWidget, self).__init__()
        self.parent = parent
        self.tracker = tracker

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        _comboBoxList = []
        _labelList = []

        for i in range(len(optionLists)):
            optionList = optionLists[i]

            _comboBoxList.append(QComboBox())
            _comboBoxList[i].addItems(optionList)
            self.layout.addWidget(_comboBoxList[i], i, 1)
            _labelList.append(QLabel(""))
            self.layout.addWidget(_labelList[i], i, 0)

        self.pickTop = _comboBoxList[0]
        self.pickBot = _comboBoxList[-1]
        self.nameTop = _labelList[0]
        self.nameBot = _labelList[-1]
    
    def applySelections(self, selections):
        for selection in selections:
            index = getattr(self, f"{selection}_index")
            self.parent.config["SELECTED_INDEX"][selection] = index
            editSelectionConfig(index, selection)

class LanguagePicker(BasePicker):
    def __init__(self, parent, tracker):
        config = parent.config
        listTop = config["LANGUAGE"]
        listBot = config["ORIENTATION"]
        optionLists = [listTop, listBot]

        super().__init__(parent, tracker, optionLists)
        self.pickTop.currentIndexChanged.connect(self.changeLanguage)
        self.pickTop.setCurrentIndex(config["SELECTED_INDEX"]["language"])
        self.nameTop.setText("Language: ")
        self.pickBot.currentIndexChanged.connect(self.changeOrientation)
        self.pickBot.setCurrentIndex(config["SELECTED_INDEX"]["orientation"])
        self.nameBot.setText("Orientation: ")

        self.language_index = self.pickTop.currentIndex()
        self.orientation_index = self.pickBot.currentIndex()

    def changeLanguage(self, i):
        self.language_index = i
        selectedLanguage = self.pickTop.currentText().strip()
        if selectedLanguage == "Japanese":
            self.tracker.language = "jpn"
        if selectedLanguage == "Korean":
            self.tracker.language = "kor"
        if selectedLanguage == "Chinese SIM":
            self.tracker.language = "chi_sim"
        if selectedLanguage == "Chinese TRA":
            self.tracker.language = "chi_tra"
        if selectedLanguage == "English":
            self.tracker.language = "eng"

    def changeOrientation(self, i):
        self.orientation_index = i
        selectedOrientation = self.pickBot.currentText().strip()
        if selectedOrientation == "Vertical":
            self.tracker.orientation = "_vert"
        if selectedOrientation == "Horizontal":
            self.tracker.orientation = ""

    def applyChanges(self):
        self.applySelections(['language', 'orientation'])
        return True

class FontPicker(BasePicker):
    def __init__(self, parent, tracker):
        config = parent.config
        listTop = config["FONT_STYLE"]
        listBot = config["FONT_SIZE"]
        optionLists = [listTop, listBot]

        super().__init__(parent, tracker, optionLists)
        self.pickTop.currentIndexChanged.connect(self.changeFontStyle)
        self.pickTop.setCurrentIndex(config["SELECTED_INDEX"]["font_style"])
        self.nameTop.setText("Font Style: ")
        self.pickBot.currentIndexChanged.connect(self.changeFontSize)
        self.pickBot.setCurrentIndex(config["SELECTED_INDEX"]["font_size"])
        self.nameBot.setText("Font Size: ")

        self.fontStyleText = "  font-family: 'Poppins';\n"
        self.fontSizeText = "  font-size: 16pt;\n"
        self.font_style_index = self.pickTop.currentIndex()
        self.font_size_index = self.pickBot.currentIndex()

    def changeFontStyle(self, i):
        self.font_style_index = i
        selectedFontStyle = self.pickTop.currentText().strip()
        replacementText = f"  font-family: '{selectedFontStyle}';\n"
        self.fontStyleText = replacementText

    def changeFontSize(self, i):
        self.font_size_index = i
        selectedFontSize = int(self.pickBot.currentText().strip())
        replacementText = f"  font-size: {selectedFontSize}pt;\n"
        self.fontSizeText = replacementText

    def applyChanges(self):
        self.applySelections(['font_style', 'font_size'])
        editStylesheet(41, self.fontStyleText)
        editStylesheet(42, self.fontSizeText)
        return True

class ScaleImagePicker(BasePicker):
    def __init__(self, parent, tracker):
        config = parent.config
        listTop = config["IMAGE_SCALING"]
        optionLists = [listTop]

        super().__init__(parent, tracker, optionLists)
        self.pickTop.currentIndexChanged.connect(self.changeScaling)
        self.pickTop.setCurrentIndex(config["SELECTED_INDEX"]["image_scaling"])
        self.nameTop.setText("Image Scaling: ")

        self.image_scaling_index = self.pickTop.currentIndex()

    def changeScaling(self, i):
        self.image_scaling_index = i

    def applyChanges(self):
        self.applySelections(['image_scaling'])
        self.parent.canvas.setViewImageMode(self.image_scaling_index)
        return True

class ShortcutPicker(BasePicker):
    def __init__(self, parent, tracker):
        config = parent.config
        listTop = config["MODIFIER"]
        optionLists = [listTop]

        super().__init__(parent, tracker, optionLists)
        self.pickTop.currentIndexChanged.connect(self.changeModifier)
        self.pickTop.setCurrentIndex(config["SELECTED_INDEX"]["modifier"])
        self.nameTop.setText("Modifier: ")

        self.pickBot = QLineEdit(config["SHORTCUT"]["capture_external_key"])
        self.layout.addWidget(self.pickBot, 1, 1)
        self.nameBot = QLabel("Key: ")
        self.layout.addWidget(self.nameBot, 1, 0)

        self.modifier_index = self.pickTop.currentIndex()

    def keyInvalidError(self):
        MessagePopup(
            "Invalid Key",
            "Please select an alphanumeric key."
        ).exec()

    def changeModifier(self, i):
        self.modifier_index = i

    def setShortcut(self, keyName, modifierText, keyText):

        tooltip = f"{self.parent.config['SHORTCUT'][f'{keyName}_tip']}{modifierText}{keyText}."
        self.parent.config["SHORTCUT"][keyName] = f"{modifierText}{keyText}"
        self.parent.config["SHORTCUT"][f"{keyName}_key"] = keyText
        self.parent.config["TBAR_FUNCS"]["FILE"][f"{keyName}_helper"]["help_msg"] = tooltip

    def applyChanges(self):
        selectedModifier = self.pickTop.currentText().strip() + "+"
        if selectedModifier == "No Modifier+":
            selectedModifier = ""

        if not self.pickBot.text().isalnum():
            self.keyInvalidError()
            return False
        if len(self.pickBot.text()) != 1:
            self.keyInvalidError()
            return False

        self.setShortcut('capture_external', selectedModifier, self.pickBot.text())
        self.applySelections(['modifier'])
        return True

class PickerPopup(QDialog):
    def __init__(self, widget):
        super(QDialog, self).__init__(None, 
            Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.widget = widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(widget)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout().addWidget(self.buttonBox)

        self.buttonBox.rejected.connect(self.cancelClickedEvent)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)        

    def accept(self):
        if self.widget.applyChanges():
            return super().accept()

    def cancelClickedEvent(self):
        self.close()