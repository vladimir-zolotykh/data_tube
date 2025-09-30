#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Generator
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


def iter_files(paths):
    for path in paths:
        if path.endswith(".gz"):
            fd = gzip.open(path)
        elif path.endswith(".bz2"):
            fd = bz2.open(path)
        else:
            fd = open(path, "rt")
        with fd as file:
            yield file


def cat_lines(files):
    for file in files:
        for line in file:
            yield line


def filter_lines(file, pattern: str = "(?i)python"):
    for line in file:
        line = line.decode("utf-8") if isinstance(line, bytes) else line
        if re.search(pattern, line):
            yield line


if __name__ == "__main__":
    lognames = iter_lognames()
    files = iter_files(lognames)
    lines = cat_lines(files)
    for line in filter_lines(lines):
        print(line)
