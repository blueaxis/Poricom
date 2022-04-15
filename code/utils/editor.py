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

from utils.config import cfg

def editConfig(index, replacement_text, config="utils/config.py"):
    with open(config, 'r') as fh:
        lines = fh.readlines()
        lines[index] = replacement_text
    with open(config, 'w') as fh:
        fh.writelines(lines)

def editCBoxConfig(index, cbox_name, config="utils/config.py"):
    replacement_text = f"    '{cbox_name}': {index},\n"
    picker_index = cfg["PICKER_INDEX"][f"{cbox_name}"]
    with open(config, 'r') as fh:
        lines = fh.readlines()
        lines[picker_index] = replacement_text
    with open(config, 'w') as fh:
        fh.writelines(lines)

def editPreviewStyle(index, replacement_text):
    ss_light = './assets/styles.qss'
    ss_dark = './assets/styles-dark.qss'
    with open(ss_light, 'r') as sl_fh, open(ss_dark, 'r') as sd_fh:
        lines_light = sl_fh.readlines()
        lines_dark = sd_fh.readlines()
        lines_light[index] = replacement_text
        lines_dark[index] = replacement_text
    with open(ss_light, 'w') as sl_fh, open(ss_dark, 'w') as sd_fh:
        sl_fh.writelines(lines_light)
        sd_fh.writelines(lines_dark)