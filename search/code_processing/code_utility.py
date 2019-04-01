#coding=utf-8
import os
import re
import uuid
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

def cpp_head_remove(code_text):
    # 去除C++头文件代码
    code_str = []
    for line in code_text.splitlines():
        if line.find('#include') != -1 or line.find('# include') != -1:
            continue
        code_str.append(line)
    code_str = '\n'.join(code_str)
    return code_str

def cpp_head_convert(code_text):
    # 将C++代码头文件中的'<'换成'&lt;', '>'换成'&gt;', 防止前端显示不出来'<'和'>'.
    code_str = []
    for line in code_text.splitlines():
        # if line.find('#include') != -1 or line.find('# include') != -1:
        #     line = line.replace("<", "&lt;")
        #     line = line.replace(">", "&gt;")
        if line.find('<') != -1:
            line = line.replace("<", "&lt;")
        if line.find('>') != -1:
            line = line.replace(">", "&gt;")
        code_str.append(line)
    code_str = '\n'.join(code_str)
    return code_str

def remove_comment(code_text):
    if type(code_text) == type([]):
        lines = code_text
    else:
        lines = code_text.split('\n')
    output_string = ''
    _map = { }
    for line in lines:
        while True:
            #这里要注意，我用的是re.S 比如print("aaa\n")
            m = re.compile('\".*\"', re.S)
            _str = m.search( line )
            #如果没匹配成功，就合并，然后下一行
            if None == _str:
                if type(code_text) == type([]):
                    output_string += line
                else:
                    output_string += line + "\n"
                break
            key = str( uuid.uuid1() )

            m = re.compile('\".*\"', re.S)
            output_tmp = re.sub(m, key, line, 1)
            line = output_tmp
            _map[ key ] = _str.group(0)

    m = re.compile(r'//.*')
    output_tmp = re.sub(m, ' ', output_string)
    output_string = output_tmp

    m = re.compile(r'/\*.*?\*/', re.S)
    output_tmp = re.sub(m, ' ', output_string)
    output_string = output_tmp

    for key in _map.keys():
        output_string = output_string.replace(key, _map[key])

    return output_string









