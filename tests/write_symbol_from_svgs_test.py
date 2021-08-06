"""Tests for vf2symbols.write_symbol_from_svgs"""
from absl.testing import flagsaver
from absl import flags

import pytest
import sys

from vf2symbols import write_symbol_from_svgs


def test_multiple_svg_matches_baseline(tmpdir):
    flags.FLAGS(sys.argv)
    actual_output = tmpdir / "temp_file"
    with flagsaver.flagsaver(out=actual_output):
        write_symbol_from_svgs.main(
            [
                "",
                "Regular-S=./tests/20px.svg",
                "Regular-M=./tests/24px.svg",
                "Regular-L=./tests/40px.svg",
            ]
        )
    with open(actual_output) as actual, open(
        "./tests/regular_sml_baseline.svg"
    ) as expected:
        assert actual.read() == expected.read()
