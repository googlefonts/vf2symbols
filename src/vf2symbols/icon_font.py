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
"""Helpers for  icon fonts."""

import functools


def wght_range(ttfont):
    os2_wght = ttfont["OS/2"].usWeightClass
    wght_range = range(os2_wght, os2_wght + 1)
    if "fvar" in ttfont:
        wght = next(filter(lambda a: a.axisTag == "wght", ttfont["fvar"].axes), None)
        wght_range = range(int(wght.minValue), int(wght.maxValue) + 1)
    return wght_range


def _cmap(ttfont):
    def _reducer(acc, u):
        acc.update(u)
        return acc

    unicode_cmaps = (t.cmap for t in ttfont["cmap"].tables if t.isUnicode())
    return functools.reduce(_reducer, unicode_cmaps, {})


def _ligature_roots(ttfont):
    lookups = tuple(
        filter(lambda l: l.LookupType == 4, ttfont["GSUB"].table.LookupList.Lookup)
    )
    assert len(lookups) == 1, "Must have exactly one ligature lookup"
    lookup = lookups[0]
    assert lookup.SubTableCount == 1  # solving only narrow case
    return lookup.SubTable[0].ligatures


def resolve_ligature(ttfont, icon_name):
    cmap = _cmap(ttfont)
    rev_cmap = {v: k for k, v in _cmap(ttfont).items()}
    first_glyph_name = cmap[ord(icon_name[0])]
    rest_of_glyph_names = [cmap[ord(c)] for c in icon_name[1:]]
    ligatures = _ligature_roots(ttfont)[first_glyph_name]
    return next(
        filter(lambda l: l.Component == rest_of_glyph_names, ligatures)
    ).LigGlyph


def extract_icon_names(ttfont, name_filter):
    rev_cmap = {v: k for k, v in _cmap(ttfont).items()}

    for first_glyph_name, ligatures in _ligature_roots(ttfont).items():
        for ligature in ligatures:
            glyph_names = (first_glyph_name,) + tuple(ligature.Component)
            icon_name = "".join(chr(rev_cmap[n]) for n in glyph_names)
            if name_filter.search(icon_name):
                yield icon_name
