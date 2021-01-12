"""Tests for vf2symbols.write_symbol_from_svg"""
from absl.testing import flagsaver
from absl import flags

import pytest
import sys

from vf2symbols import write_symbol_from_svg


def test_single_svg_matches_baseline(tmpdir):
    flags.FLAGS(sys.argv)
    actual_output = tmpdir / "temp_file"
    with flagsaver.flagsaver(out=actual_output):
        write_symbol_from_svg.main(["", "./tests/sample.svg"])
    with open(actual_output) as actual, open(
        "./tests/sample_symbol_baseline.svg"
    ) as expected:
        assert actual.read() == expected.read()
