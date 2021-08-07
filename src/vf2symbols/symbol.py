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

from typing import Any

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from lxml import etree  # pytype: disable=import-error
from picosvg.geometric_types import Rect
from picosvg.svg import SVG
from picosvg.svg_transform import Affine2D

_SYMBOL_SIZE = 120
# https://developer.apple.com/documentation/uikit/uiimage/creating_custom_symbol_images_for_your_app#3369941
_SYMBOL_SCALE = {"S": 0.789, "M": 1, "L": 1.29}
# (Capline Y - Baseline Y ) / 2
_CENTER_LINE = -35.23

_SYMBOL_FILEPATH = os.path.join(os.path.dirname(__file__), "symbol_template.svg")


class Symbol:
    def __init__(self, symbol_filepath=_SYMBOL_FILEPATH):
        self.symbol = SVG.parse(symbol_filepath)

    def write_icon(
        self, symbol_name: str, drawable_path: Any, svg_pen: SVGPathPen, rect: Rect
    ) -> None:
        """Writes a drawable object to the current symbol.

        Args:
          symbol_name: Symbol variant name to place the symbol at (e.g.
            Regular-M).
          drawable_path: Any drawable object that supports the FontTools pen
            protocol (e.g. SVGPath).
          svg_pen: SVGPathPen for drawing the path.
          rect: The bounding box co-ordinates of the given svg_path used to
            position the drawable object correctly in the symbol space, for
            example, in the icon fonts where the Y-axis is flipped, the height
            is expected to be -ve.
        """
        parent = self.symbol.xpath_one(f'//svg:g[@id="{symbol_name}"]')
        path = etree.SubElement(parent, "path")
        path.attrib["d"] = self._draw_svg_path(
            drawable_path, svg_pen, self._build_transformation(symbol_name, rect)
        )

    def _draw_svg_path(self, svg_path, svg_pen, transform):
        svg_path.draw(TransformPen(svg_pen, transform))
        return " ".join(svg_pen._commands)

    def _build_transformation(self, symbol_name, rect):
        symbol_size = self._symbol_size(symbol_name)
        return Affine2D.rect_to_rect(
            rect, Rect(0, _CENTER_LINE - (symbol_size / 2), symbol_size, symbol_size)
        )

    def _symbol_size(self, symbol):
        return _SYMBOL_SCALE[symbol[-1]] * _SYMBOL_SIZE

    def drop_empty_icons(self):
        for empty_icon in self.symbol.xpath(f"//svg:g[not(*)]"):
            empty_icon.getparent().remove(empty_icon)

    def write_to(self, filename):
        if filename:
            with open(filename, "w") as f:
                f.write(self.symbol.tostring())
        else:
            print(self.symbol.tostring())
