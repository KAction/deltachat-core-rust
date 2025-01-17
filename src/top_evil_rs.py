#!/usr/bin/env python3


from pathlib import Path
import os
import re

if __name__ == "__main__":
    if Path('src/top_evil_rs.py').exists():
        os.chdir('src')
    filestats = []
    for fn in Path(".").glob("**/*.rs"):
        s = fn.read_text()
        s = re.sub(r"(?m)///.*$", "", s)  # remove comments
        unsafe = s.count("unsafe")
        free = s.count("free(")
        gotoblocks = s.count("ok_to_continue") + s.count('OK_TO_CONTINUE')
        filestats.append((fn, unsafe, free, gotoblocks))

    sum_unsafe, sum_free, sum_gotoblocks = 0, 0, 0

    for fn, unsafe, free, gotoblocks in reversed(sorted(filestats, key=lambda x: sum(x[1:]))):
        print("{0: <30} unsafe: {1: >3} free: {2: >3} ok_to_continue: {3: >3}".format(str(fn), unsafe, free, gotoblocks))
        sum_unsafe += unsafe
        sum_free += free
        sum_gotoblocks += gotoblocks


    print()
    print("total unsafe:", sum_unsafe)
    print("total free:", sum_free)
    print("total ok_to_continue:", sum_gotoblocks)

