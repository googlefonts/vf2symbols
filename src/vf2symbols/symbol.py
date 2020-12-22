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

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from lxml import etree  # pytype: disable=import-error
from nanoemoji import color_glyph
from picosvg.geometric_types import Rect
from picosvg.svg import SVG

_SYMBOL_SIZE = 120
_SYMBOL_DY_MULTIPLE = 0.7942


class Symbol():

    def __init__(self):
        self.symbol = SVG.parse(os.path.join(os.path.dirname(__file__), "symbol_template.svg"))

    
    def write_icon(self, symbol_wght_name, svg_path, svg_pen, x_size, y_size, from_font=False):
        parent = self.symbol.xpath_one(f'//svg:g[@id="{symbol_wght_name}"]')
        path = etree.SubElement(parent, "path")
        path.attrib["d"] = self._draw_svg_path(svg_path, svg_pen, self._build_transformation(from_font, x_size, y_size))
        
        
    def _draw_svg_path(self, svg_path, svg_pen, transform):
        svg_path.draw(TransformPen(svg_pen, transform))
        return " ".join(svg_pen._commands) 
       
        
    def _build_transformation(self, from_font, x_size, y_size):
        if from_font:
            return Transform(*color_glyph.map_viewbox_to_font_emsquare(Rect(0, 0, x_size, y_size), _SYMBOL_SIZE)).translate(0,_SYMBOL_DY_MULTIPLE * y_size)
        else:
            return Transform(_SYMBOL_SIZE/x_size, 0, 0, _SYMBOL_SIZE/y_size, 0, 0).translate(0,-_SYMBOL_DY_MULTIPLE * y_size)
        
              
    def drop_empty_icons(self):
        for empty_icon in self.symbol.xpath(f"//svg:g[not(*)]"):
            empty_icon.getparent().remove(empty_icon)
    
    
    def write_to(self, filename):
        with open(filename, "w") as f:
            f.write(self.symbol.tostring())

