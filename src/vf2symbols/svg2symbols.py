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
"""Create a set of Apple custom symbols from static SVGs.

Places the static SVG in the 'Regular-M' required variant of the iOS symbol.
"""
import os
import re
import subprocess
import sys

from absl import app
from absl import flags
from absl import logging

from ninja import ninja_syntax

FLAGS = flags.FLAGS

# internal flags, typically client wouldn't change
flags.DEFINE_string("build_dir", "build/", "Where build runs.")
flags.DEFINE_bool("gen_ninja", True, "Whether to regenerate build.ninja")
flags.DEFINE_bool("exec_ninja", True, "Whether to run ninja.")


def _write_svg_preamble(nw):
    def module_rule(mod_name, arg_pattern):
        nw.rule(mod_name, f"{sys.executable} -m vf2symbols.{mod_name} {arg_pattern}")

    nw.comment("Generated by svg2symbols")
    nw.newline()

    module_rule("write_symbol_from_svg", "--out $out $in")


def _write_svg_symbol_builds(nw, svgs):
    for svg in svgs:
        output = re.sub(r"([.]\w+)$", "_symbol\\1", svg)
        nw.build(output, "write_symbol_from_svg", svg)


def _run(argv):
    if len(argv) < 2:
        sys.exit("Expected list of SVG filepath")

    os.makedirs(FLAGS.build_dir, exist_ok=True)
    build_file = os.path.join(FLAGS.build_dir, "build.ninja")
    if FLAGS.gen_ninja:
        logging.info(f"Generating %s", os.path.relpath(build_file))
        with open(build_file, "w") as f:
            nw = ninja_syntax.Writer(f)
            _write_svg_preamble(nw)
            _write_svg_symbol_builds(nw, argv[1:])

    ninja_cmd = ["ninja", "-C", os.path.dirname(build_file)]
    if FLAGS.exec_ninja:
        print(" ".join(ninja_cmd))
        subprocess.run(ninja_cmd, check=True)
    else:
        print("To run:", " ".join(ninja_cmd))


def main():
    # We don't seem to be __main__ when run as cli tool installed by setuptools
    app.run(_run)


if __name__ == "__main__":
    app.run(_run)
