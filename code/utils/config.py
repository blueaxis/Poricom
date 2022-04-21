"""
Poricom Configuration Utilities

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

import toml
config = toml.load("./utils/config.toml")

def saveOnClose(data, config="utils/config.toml"):
    with open(config, 'w') as fh:
        toml.dump(data, fh)

def editConfig(index, replacement_text, config="utils/config.toml"):
    data = toml.load(config)
    data[index] = replacement_text
    with open(config, 'w') as fh:
        toml.dump(data, fh)

def editSelectionConfig(index, cbox_name, config="utils/config.toml"):
    data = toml.load(config)
    data["SELECTED_INDEX"][cbox_name] = index
    with open(config, 'w') as fh:
        toml.dump(data, fh)

def editStylesheet(index, replacement_text):
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