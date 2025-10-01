#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Generator, TextIO
from typing import NamedTuple
import os
import fnmatch
import bz2
import gzip
import re
import argparse
import argcomplete
import psutil


class Line(NamedTuple):
    path: str
    lineno: int
    line: str


def iter_lognames(
    top: str = "www", pattern: str = "access-log*"
) -> Generator[str, None, None]:
    for path, _, names in os.walk(top):
        for name in fnmatch.filter(names, pattern):
            yield os.path.join(path, name)


def iter_files(paths: Generator[str, None, None]) -> Generator[TextIO, None, None]:
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


def cat_lines(files: Generator[TextIO, None, None]) -> Generator[Line, None, None]:
    for file in files:
        fname = getattr(file, "name", "<unknown>")
        for lineno, line in enumerate(file, 1):
            yield Line(fname, lineno, line)


def filter_lines(
    lines: Generator[Line, None, None], pattern: str = "(?i)python"
) -> Generator[Line, None, None]:
    for line in lines:
        if re.search(pattern, line.line):
            yield line


parser = argparse.ArgumentParser(
    description="""\
Chain Python generators (like a Unix data pipeline)""",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("--log-dir", help="Top dir of log files tree", default="./www")
parser.add_argument(
    "--cmd", choices=["print", "count-bytes"], help="Select command", default="print"
)
parser.add_argument("--fname-pattern", help="Select log files", default="access-log*")
parser.add_argument("--search-pattern", help="Select log lines", default="(?i)python")
parser.add_argument("--count-open-files", help="Count open files", action="store_true")


def count_open_files() -> int:
    proc = psutil.Process(os.getpid())
    return len(proc.open_files())


if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    lognames = iter_lognames(args.log_dir, args.fname_pattern)
    files = iter_files(lognames)
    lines = cat_lines(files)
    if args.cmd == "print":
        print(type(lines))
        for line in filter_lines(lines, args.search_pattern):
            print(line.line, end="")
    elif args.cmd == "count-bytes":
        bytes_column = (line.line.rsplit(None, 1)[1] for line in lines)
        total: int = sum(int(count) for count in bytes_column if count != "-")
        # Print total number of transferred bytes in matched lines
        print("Total: ", total)
    else:
        raise TypeError(
            f"{args.cmd}: Invalid command. Expected 'print' or 'count-bytes'"
        )
    if args.count_open_files:
        print("Open files: ", count_open_files())
