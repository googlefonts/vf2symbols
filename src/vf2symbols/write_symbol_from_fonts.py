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

"""Generates an Apple custom symbol using one or more font instances."""

from absl import app
from absl import flags
from absl import logging
from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools import ttLib
from lxml import etree  # pytype: disable=import-error
from nanoemoji import color_glyph
import os
from picosvg.geometric_types import Rect
from picosvg.svg import SVG
from vf2symbols import icon_font
from vf2symbols.symbol import Symbol

FLAGS = flags.FLAGS


# internal flags, typically client wouldn't change
flags.DEFINE_string("out", None, "Output file.")


# Borrowed from nanoemoji tests/colr_to_svg.py
def _map_font_to_viewbox(upem: int, view_box: Rect):
    if view_box != Rect(0, 0, view_box.w, view_box.w):
        raise ValueError("We simply must have a SQUARE from 0,0")
    affine = color_glyph.map_viewbox_to_font_emsquare(
        Rect(0, 0, upem, upem), view_box.w
    )
    return Transform(*affine)

def _draw_svg_path(ttfont, icon_name, dest_region):
    glyph_name = icon_font.resolve_ligature(ttfont, icon_name)
    upem = ttfont["head"].unitsPerEm
    transform = _map_font_to_viewbox(upem, dest_region)
    transform = transform.translate(0, 0.7942 * upem)

    svg_pen = SVGPathPen(ttfont.getGlyphSet())
    ttfont.getGlyphSet()[glyph_name].draw(TransformPen(svg_pen, transform))
    return " ".join(svg_pen._commands)


def main(argv):
    icon_name = os.path.splitext(os.path.basename(FLAGS.out))[0]
    dest_region = Rect(0, 0, 120, 120)

    symbol = Symbol()

    for font_filename in argv[1:]:
        ttfont = ttLib.TTFont(font_filename)
        svg_path = _draw_svg_path(ttfont, icon_name, dest_region)
        ttfont.close()
        symbol_wght_name = font_filename.split(".")[-2]
        symbol.write_icon(symbol_wght_name, svg_path)

    symbol.drop_empty_icons()
    symbol.write_to(FLAGS.out)


if __name__ == "__main__":
    app.run(main)
