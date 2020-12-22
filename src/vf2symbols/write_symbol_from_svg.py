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
import re

from absl import app
from absl import flags
from absl import logging

from fontTools import svgLib
from fontTools.pens.svgPathPen import SVGPathPen
from picosvg.svg import SVG
from vf2symbols.symbol import Symbol

_REQUIRED_SYMBOL = "Regular-M"

FLAGS = flags.FLAGS

# internal flags, typically client wouldn't change
flags.DEFINE_string("out", None, "Output file.")


def parse_float(string):
    return float(re.compile("\d+([.]\d*)?").match(string).group(0))
    

def main(argv):
    if len(argv) > 2:
        sys.exit("Expected Only 1 non-flag Argument.")
    symbol = Symbol()
    pico = SVG.parse(argv[1]).topicosvg()
    main_svg = pico.xpath_one("//svg:svg")
    symbol.write_icon(_REQUIRED_SYMBOL, svgLib.SVGPath.fromstring(pico.tostring()), SVGPathPen(None), parse_float(main_svg.get("width")), parse_float(main_svg.get("height")))
    symbol.drop_empty_icons()
    symbol.write_to(FLAGS.out)
    

if __name__ == "__main__":
    app.run(main)
