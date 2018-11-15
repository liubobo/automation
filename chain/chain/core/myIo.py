import sys
from io import StringIO
from viewList import vList


def simulate(str):
    strio = StringIO(str)
    sys.stdin = strio


def readlines_from_stdin():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if isinstance(line, str):
            line = line.decode(encoding='utf-8')
        lines.append(line)
    return lines