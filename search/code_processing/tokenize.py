#coding=utf-8
import re
import os
import keyword
import tempfile
import jieba
# from .code_utility import remove_comment
# from .relate_dict import python_buildin_function, cpp_buildin_function, cpp_keywords
from code_utility import remove_comment
from relate_dict import python_buildin_function, cpp_buildin_function, cpp_keywords

py_keywords = keyword.kwlist                    # Python内部保留字
py_buildin_function = python_buildin_function   # Python内嵌函数
cpp_keywords = cpp_keywords                     # C++内部保留字
cpp_buildin_function = cpp_buildin_function     # C++内嵌函数
need_words = py_keywords + python_buildin_function + cpp_keywords + cpp_buildin_function

def alone_char(char, text):
    # 判断一个字符char在一个字符串中是独立存在的单字符单词, 还是其中某个单词的一部分.
    pass

def highlight_words(code_text, highlight = False):
    # 提取出需要高亮的单词
    identifier = r'[a-zA-Z]{0,30}'  # 标识符正则表达式
    p = re.compile(identifier)
    words = p.findall(code_text)
    code_str = re.sub(r'[\s]', ' ', ' '.join(words))
    code_str = code_str.split()
    # if highlight == True:
        # code_str = [word for word in code_str if len(word) != 1]
    code_str = ' '.join(code_str)
    return code_str


EXACT_TOKEN_TYPES = {
    'comment': 'COMMENT',
    'nl': 'NL',
    'encoding': 'ENCODING',
    'ASYNC': 'ASYNC',
    'value': 'value',
    'name': 'name',
    'AWAIT': 'AWAIT',
    'DEDENT': 'DEDENT',
    'ELLIPSIS': 'ELLIPSIS',
    'ENDMARKER': 'ENDMARKER',
    'ERRORTOKEN': 'ERRORTOKEN',
    'INDENT': 'INDENT',
    'N_TOKENS': 'N_TOKENS',
    'NAME': 'NAME',
    'NEWLINE': 'NEWLINE',
    'NT_OFFSET': 'NT_OFFSET',
    'NUMBER': 'NUMBER',
    'OP': 'OP',
    'RARROW': 'RARROW',
    'STRING': 'STRING',
    'tok_name': 'tok_name',
    '(':   'LPAR',
    ')':   'RPAR',
    '[':   'LSQB',
    ']':   'RSQB',
    ':':   'COLON',
    ',':   'COMMA',
    ';':   'SEMI',
    '+':   'PLUS',
    '-':   'MINUS',
    '*':   'STAR',
    '/':   'SLASH',
    '|':   'VBAR',
    '||':    'DOUBLEVBAR',
    '&':   'AMPER',
    '&&':  'DOUBLEAMPER',
    '<':   'LESS',
    '>':   'GREATER',
    '=':   'EQUAL',
    '.':   'DOT',
    '%':   'PERCENT',
    '{':   'LBRACE',
    '}':   'RBRACE',
    '==':  'EQEQUAL',
    '!=':  'NOTEQUAL',
    '<=':  'LESSEQUAL',
    '>=':  'GREATEREQUAL',
    '~':   'TILDE',
    '^':   'CIRCUMFLEX',
    '<<':  'LEFTSHIFT',
    '>>':  'RIGHTSHIFT',
    '**':  'DOUBLESTAR',
    '+=':  'PLUSEQUAL',
    '-=':  'MINEQUAL',
    '*=':  'STAREQUAL',
    '/=':  'SLASHEQUAL',
    '%=':  'PERCENTEQUAL',
    '&=':  'AMPEREQUAL',
    '|=':  'VBAREQUAL',
    '^=':  'CIRCUMFLEXEQUAL',
    '<<=': 'LEFTSHIFTEQUAL',
    '>>=': 'RIGHTSHIFTEQUAL',
    '**=': 'DOUBLESTAREQUAL',
    '//':  'DOUBLESLASH',
    '//=': 'DOUBLESLASHEQUAL',
    '@':   'AT',
    '@=':  'ATEQUAL',
    "'": 'QUOTE',
    '"': 'DOUBLEQUOTE',
}

punctuation_replace_dict = {
    "'": 'QT',
    '"': 'DQT',
    '(': 'AW',
    ')': 'AX',
    '[': 'AY',
    ']': 'AZ',
    ':': 'B0',
    ',': 'BD',
    ';': 'BE',
    '+': 'BF',
    '-': 'BG',
    '*': 'BH',
    '/': 'BI',
    '|': 'BJ',
    '||':  'DBJ',
    '&': 'BK',
    '&&':  'DBK',
    '<': 'BL',
    '>': 'BM',
    '=': 'BN',
    '.': 'BO',
    '%': 'BP',
    '{': 'BQ',
    '}': 'BR',
    '==': 'BS',
    '!=': 'BT',
    '<=': 'BU',
    '>=': 'BV',
    '~': 'BW',
    '^': 'BX',
    '<<': 'BY',
    '>>': 'BZ',
    '**': 'CD',
    '+=': 'CE',
    '-=': 'CF',
    '*=': 'CG',
    '/=': 'CH',
    '%=': 'CI',
    '&=': 'CJ',
    '|=': 'CK',
    '^=': 'CL',
    '<<=': 'CM',
    '>>=': 'CN',
    '**=': 'CO',
    '//': 'CP',
    '//=': 'CQ',
    '@': 'CR',
    '@=': 'CS',
}

replace_dict = {
    'COMMENT': 'AB',
    'NL': 'AC',
    'ENCODING': 'AD',
    'ASYNC': 'AE',
    'value': 'AF',
    'name': 'AG',
    'AWAIT': 'AH',
    'DEDENT': 'AI',
    'ELLIPSIS': 'AJ',
    'ENDMARKER': 'AK',
    'ERRORTOKEN': 'AL',
    'INDENT': 'AM',
    'N_TOKENS': 'AN',
    'NAME': 'AO',
    'NEWLINE': 'AP',
    'NT_OFFSET': 'AQ',
    'NUMBER': 'AR',
    'OP': 'AS',
    'RARROW': 'AT',
    'STRING': 'AU',
    'tok_name': 'AV',
    'LPAR':   'AW',
    'RPAR':   'AX',
    'LSQB':   'AY',
    'RSQB':   'AZ',
    'COLON':   'B0',
    'COMMA':   'BD',
    'SEMI':   'BE',
    'PLUS':   'BF',
    'MINUS':   'BG',
    'STAR':   'BH',
    'SLASH':   'BI',
    'VBAR':   'BJ',
    'DOUBLEVBAR': 'DBJ',
    'AMPER':   'BK',
    'DOUBLEAMPER': 'DBK',
    'LESS':   'BL',
    'GREATER':   'BM',
    'EQUAL':   'BN',
    'DOT':   'BO',
    'PERCENT':   'BP',
    'LBRACE':   'BQ',
    'RBRACE':   'BR',
    'EQEQUAL':  'BS',
    'NOTEQUAL':  'BT',
    'LESSEQUAL':  'BU',
    'GREATEREQUAL':  'BV',
    'TILDE':   'BW',
    'CIRCUMFLEX':   'BX',
    'LEFTSHIFT':  'BY',
    'RIGHTSHIFT':  'BZ',
    'DOUBLESTAR':  'CD',
    'PLUSEQUAL':  'CE',
    'MINEQUAL':  'CF',
    'STAREQUAL':  'CG',
    'SLASHEQUAL':  'CH',
    'PERCENTEQUAL':  'CI',
    'AMPEREQUAL':  'CJ',
    'VBAREQUAL':  'CK',
    'CIRCUMFLEXEQUAL':  'CL',
    'LEFTSHIFTEQUAL': 'CM',
    'RIGHTSHIFTEQUAL': 'CN',
    'DOUBLESTAREQUAL': 'CO',
    'DOUBLESLASH':  'CP',
    'DOUBLESLASHEQUAL': 'CQ',
    'AT':   'CR',
    'ATEQUAL':  'CS',
    'DOUBLEQUOTE': 'DQT',
    'QUOTE': 'QT',
}

jieba.load_userdict(punctuation_replace_dict.keys())

def tokenize(code_text, char_or_lex):
    # 将代码转换成一个token串, 即进行词法分析之后的结果
    returned_string = ""
    code_text = remove_comment(code_text)
    filter_token = ['ENCODING', 'NL', 'NEWLINE', 'COMMENT', 'ENDMARKER', 'INDENT', 'DEDENT', 'ERRORTOKEN']
    all_punctuation = punctuation_replace_dict.keys()
    if char_or_lex == 'char':
        code_text = code_text.replace('\n', ' ')
        code_text_list = list(jieba.cut(code_text))
        for word in code_text_list:
            if word.strip() != "":
                if word in all_punctuation:
                    returned_string += ("punc_" + punctuation_replace_dict[word] + " ")
                else:
                    returned_string += ("char_" + word + " ")
    elif char_or_lex == 'lex':
        with tempfile.NamedTemporaryFile('w+t', suffix='.txt') as f:
            f_file = open(f.name, 'w')
            f_file.write(code_text)
            f_file = open(f.name, 'r')
            command = "python3 -m tokenize -e " + f.name
            tokens = os.popen(command).readlines()
            if len(tokens) == 0:
                # 如果词法分析失败(如括号不匹配), 则手动替换
                code_text = code_text.replace('\n', ' ')
                code_text_list = list(jieba.cut(code_text))
                for word in code_text_list:
                    if word.strip() != "":
                        if word in all_punctuation:
                            returned_string += ("punc_" + punctuation_replace_dict[word] + " ")
                        elif word in need_words:
                            returned_string += ("key_" + word + " ")
                        else:
                            returned_string += (replace_dict["NAME"] + " ")
                f_file.close()
                return returned_string

            for token in tokens:
                token = token.split()
                if len(token) == 3:
                    if token[1] in filter_token:
                        continue
                    word = eval(token[2])
                    if word in all_punctuation:
                        returned_string += ("punc_" + punctuation_replace_dict[word] + " ")
                    else:
                        if word in need_words:
                            returned_string += ("key_" + word + " ")
                        else:
                            try:
                                returned_string += (replace_dict[token[1]] + " ")
                            except:
                                returned_string += (token[1] + " ")
            f_file.close()
    return returned_string

def lex_analysis_char(code_text):
    '''将代码转换成一个连续的字符串(只去掉其中的空白字符即可)'''
    code_text = code_text.replace('\n', ' ')
    code_text = re.sub(r'[\s]', '', code_text)
    return code_text

def all_substring(code_string):
    token_list = code_string.split(" ")
    length = len(token_list)
    sub_string_list = ["_".join(token_list[i:j + 1]) for i in range(length) for j in range(i,length)]
    return " ".join(sub_string_list)

import time
code_text = '''
a = b + c
'''
# print(highlight_words(code_text))
print(tokenize(code_text, 'char'))
print(tokenize(code_text, 'lex'))

















