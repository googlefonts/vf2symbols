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
import re
import sys

from absl import app
from absl import flags

from fontTools import svgLib
from fontTools.pens.svgPathPen import SVGPathPen
from picosvg.geometric_types import Rect
from picosvg.svg import SVG
from vf2symbols.symbol import Symbol
from vf2symbols import write_symbol_from_svgs

_REQUIRED_SYMBOL = "Regular-M"



def main(argv):
    if len(argv) > 2:
        sys.exit("Expected Only 1 non-flag Argument.")
    write_symbol_from_svgs.main([argv[0], f'{_REQUIRED_SYMBOL}={argv[1]}'])


if __name__ == "__main__":
    app.run(main)
