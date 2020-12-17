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

"""Generates an Apple custom symbol using an SVG by placing it in the required variant."""
import os

from absl import app
from absl import flags
from absl import logging

from fontTools import svgLib
from fontTools.misc import transform
from fontTools.pens.svgPathPen import SVGPathPen
from lxml import etree  # pytype: disable=import-error
from nanoemoji import color_glyph
from picosvg.geometric_types import Rect
from picosvg.svg import SVG
from vf2symbols.symbol import Symbol

_REQUIRED_SYMBOL = "Regular-M"
_SYMBOL_DY = -95.23 # Centers Medium variants 

FLAGS = flags.FLAGS

# internal flags, typically client wouldn't change
flags.DEFINE_string("out", None, "Output file.")


def _draw_svg_path(svg_filename):
    pico = SVG.parse(svg_filename).topicosvg()
    main_svg = pico.xpath_one("//svg:svg")
    scale_x = 120 / float(main_svg.get("width"))
    scale_y = 120 / float(main_svg.get("height"))
    svg_path = svgLib.SVGPath.fromstring(pico.tostring(), transform.Transform(scale_x,0,0,scale_y,0,_SYMBOL_DY))
    svg_pen = SVGPathPen(None)
    svg_path.draw(svg_pen)
    return " ".join(svg_pen._commands)

  
def main(argv):
    if len(argv) > 2:
        sys.exit("Expected Only 1 non-flag Argument.")
    symbol = Symbol()
    svg_path = _draw_svg_path(argv[1])   
    symbol.write_icon(_REQUIRED_SYMBOL, svg_path)
    symbol.drop_empty_icons()
    symbol.write_to(FLAGS.out)
    

if __name__ == "__main__":
    app.run(main)
