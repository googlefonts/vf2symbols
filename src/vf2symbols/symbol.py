# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Represents an Apple custom symbol."""
import os

from lxml import etree  # pytype: disable=import-error
from picosvg.svg import SVG


class Symbol():
    def __init__(self):
        self.symbol = SVG.parse(os.path.join(os.path.dirname(__file__), "symbol_template.svg"))
        
        
    def write_icon(self, symbol_wght_name, svg_path):
        parent = self.symbol.xpath_one(f'//svg:g[@id="{symbol_wght_name}"]')
        path = etree.SubElement(parent, "path")
        path.attrib["d"] = svg_path
        
        
    def drop_empty_icons(self):
        for empty_icon in self.symbol.xpath(f"//svg:g[not(*)]"):
            empty_icon.getparent().remove(empty_icon)
    
    
    def write_to(self, filename):
        with open(filename, "w") as f:
            f.write(self.symbol.tostring())

