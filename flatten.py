#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections.abc import Iterable, Generator
from typing import Any, TypeVar, Union, Tuple, cast


logline = """\
74.6.25.144 - - [24/Feb/2008:00:48:16 -0600] "GET /dynamic/01Introduction.pdf HTTP/1.0" 200 3110734\
"""

nested_list = [1, 2, ["three", "four", ["cat", "apple"]], 4]

T = TypeVar("T")


def flatten(
    items: Iterable[Union[T, Iterable[Any]]],
    ignore_types: Tuple[type, ...] = (str, bytes),
) -> Generator[T, None, None]:
    x: T | Iterable[Any]
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x, ignore_types)
        else:
            yield cast(T, x)


if __name__ == "__main__":
    for x in flatten(nested_list):
        print(x)
