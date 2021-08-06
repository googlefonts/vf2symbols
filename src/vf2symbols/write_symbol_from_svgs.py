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
"""Generates an Apple custom symbol using SVGs.

Fills an apple symbols variants with the provided SVGs.
Takes one or more space seperated pairs of symbol name and its SVG filepath.

https://developer.apple.com/documentation/uikit/uiimage/creating_custom_symbol_images_for_your_app#3369885

Usage:
write_symbol_from_svgs.py -out [output path] [symbol_layer_name=svg_path ....]

Example:
write_symbol_from_svgs.py -out apple_symbol.svg Regular-M=regular.svg Regular-L=large.svg
"""
import re
import sys

from absl import app
from absl import flags

from fontTools import svgLib
from fontTools.pens.svgPathPen import SVGPathPen
from picosvg.geometric_types import Rect
from picosvg.svg import SVG
from vf2symbols.symbol import Symbol

FLAGS = flags.FLAGS

# internal flags, typically client wouldn't change
flags.DEFINE_string("out", None, "Output file.")


def parse_float(string):
    return float(re.compile("\d+([.]\d*)?").match(string).group(0))


def main(argv):
    if len(argv) < 2:
        sys.exit(
            "Expected at least 1 non-flag Argument of a symbol layer name and svg path pair."
        )
    symbol = Symbol()
    for arg in argv[1:]:
        layer_name, svg_path = arg.split("=")
        pico = SVG.parse(svg_path).topicosvg()
        main_svg = pico.xpath_one("//svg:svg")
        symbol.write_icon(
            layer_name,
            svgLib.SVGPath.fromstring(pico.tostring()),
            SVGPathPen(None),
            Rect(
                0,
                0,
                parse_float(main_svg.get("width")),
                parse_float(main_svg.get("height")),
            ),
        )
    symbol.drop_empty_icons()
    symbol.write_to(FLAGS.out)


if __name__ == "__main__":
    app.run(main)
