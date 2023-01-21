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


def editConfig(index, replacementText, config="utils/config.toml"):
    data = toml.load(config)
    data[index] = replacementText
    with open(config, 'w') as fh:
        toml.dump(data, fh)


def editSelectionConfig(index, cBoxName, config="utils/config.toml"):
    data = toml.load(config)
    data["SELECTED_INDEX"][cBoxName] = index
    with open(config, 'w') as fh:
        toml.dump(data, fh)
