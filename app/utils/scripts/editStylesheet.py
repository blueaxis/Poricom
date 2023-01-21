"""
Poricom Helper Functions

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

from ..constants import STYLESHEET_LIGHT, STYLESHEET_DARK

def editStylesheet(index: int, style: str):
    """
    Replace stylesheet at line `index` with input `style`
    """
    with open(STYLESHEET_LIGHT, 'r') as slFh, open(STYLESHEET_DARK, 'r') as sdFh:
        lineLight = slFh.readlines()
        linesDark = sdFh.readlines()
        lineLight[index] = style
        linesDark[index] = style
    with open(STYLESHEET_LIGHT, 'w') as slFh, open(STYLESHEET_DARK, 'w') as sdFh:
        slFh.writelines(lineLight)
        sdFh.writelines(linesDark)
