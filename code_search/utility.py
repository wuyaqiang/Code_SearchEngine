#coding=utf-8
import os
import sys
import tempfile
import logging
from lib2to3.main import main


def convert_to_py3(script):
    """将一段Python2代码转化成Python3代码"""
    if sys.version_info[0] < 3:
        return script

    f = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
    f.write(script.encode())
    f.flush()
    filename = f.name
    f.close()

    logging.basicConfig(filename=os.devnull)

    if main("lib2to3.fixes", ['--no-diffs', '-w', '-n', filename]):
        raise Exception('py3 conversion failed')

    f2 = open(filename, 'r')
    try:
        return f2.read()
    finally:
        f2.close()
        os.remove(filename)