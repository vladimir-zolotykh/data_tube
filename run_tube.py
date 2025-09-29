#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import TypeVar
from collections.abc import Iterable
import fnmatch
import bz2
import sys
import gzip
import re

logline = """\
74.6.25.144 - - [24/Feb/2008:00:48:16 -0600] "GET /dynamic/01Introduction.pdf HTTP/1.0" 200 3110734\
"""

nested_list = [1, 2, ["three", "four", ["cat", "apple"]], 4]

T = TypeVar("T")


def flatten(item: Iterable[T] | T):
    if isinstance(item, Iterable):
        x: T
        for x in item:
            yield flatten(x)
    else:
        yield item


if __name__ == "__main__":
    for x in flatten(nested_list):
        print(x)
