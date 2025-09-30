#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Generator, TextIO, BinaryIO
import os
import fnmatch
import bz2
import gzip
import re


def iter_lognames(
    top: str = "www", pattern: str = "access-log*"
) -> Generator[str, None, None]:
    for path, _, names in os.walk(top):
        for name in fnmatch.filter(names, pattern):
            yield os.path.join(path, name)


def iter_files(paths) -> Generator[TextIO, None, None]:
    for path in paths:
        fd: TextIO
        if path.endswith(".gz"):
            fd = gzip.open(path, "rt", encoding="utf-8")
        elif path.endswith(".bz2"):
            fd = bz2.open(path, "rt")
        else:
            fd = open(path, "rt")
        with fd as file:
            yield file


def cat_lines(files) -> Generator[str | bytes, None, None]:
    for file in files:
        for line in file:
            yield line


def filter_lines(file, pattern: str = "(?i)python") -> Generator[str, None, None]:
    for line in file:
        if re.search(pattern, line):
            yield line


if __name__ == "__main__":
    lognames = iter_lognames()
    files = iter_files(lognames)
    lines = cat_lines(files)
    # for line in filter_lines(lines):
    #     print(line)
    bytes_column = (line.rsplit(None, 1)[1] for line in lines)
    total: int = sum(int(count) for count in bytes_column if count != "-")
    # Print total number of transferred bytes in matched lines
    print("Total: ", total)
