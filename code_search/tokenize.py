#coding=utf-8
import re
import os
import keyword
import tempfile
# from .relate_dict import python_buildin_function, cpp_buildin_function, cpp_keywords
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
    '&':   'AMPER',
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
}

punctuation_replace_dict = {
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
    '&': 'BK',
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
    'AMPER':   'BK',
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

}

def lex_analysis(code_text):
    # 将代码转换成一个token串, 即进行词法分析之后的结果
    code_str = []
    filter_token = ['ENCODING', 'NL', 'COMMENT', 'ENDMARKER', 'INDENT', 'DEDENT', 'ERRORTOKEN']
    with tempfile.NamedTemporaryFile('w+t', suffix='.txt') as f:
        f_file = open(f.name, 'w')
        f_file.write(code_text)
        f_file = open(f.name, 'r')
        command = "python3 -m tokenize -e " + f.name
        tokens = os.popen(command).readlines()
        # if len(tokens) == 0:
        #     code_text = code_text.replace('\n', ' ')
        #     identifier = r'[a-zA-Z]{1,30}'  # 单词的正则表达式
        #     number = r'[0-9]+'
        #     code_text = re.sub(number, replace_dict['NUMBER'], code_text)
        #     p1 = re.compile(identifier)
        #     words = list(set(p1.findall(code_text)))
        #     for word in words:
        #         if word not in need_words and word not in replace_dict.values():
        #             code_text = code_text.replace(word, replace_dict['NAME'])
        #     for key, value in punctuation_replace_dict.items():
        #         code_text = code_text.replace(key, value)
        #     code_text = re.sub(r'[\s]', '', code_text)
        #     f_file.close()
        #     return code_text
        for token in tokens:
            print(token)
            token = token.split()
            if len(token) == 3:
                if token[1] in filter_token:
                    continue
                if eval(token[2]) in need_words:
                    code_str.append(eval(token[2]))
                    continue
                try:
                    code_str.append(token[1].replace(token[1], replace_dict[token[1]]))
                except:
                    code_str.append(token[1])
        f_file.close()
    return ' '.join(code_str)

def lex_analysis_char(code_text):
    # 将代码转换成一个连续的字符串(只去掉其中的空白字符即可)
    code_text = code_text.replace('\n', ' ')
    code_text = re.sub(r'[\s]', '', code_text)
    return code_text

# def lex_analysis_char(code_text):
#     code_str = []
#     filter_token = ['ENCODING', 'NL', 'COMMENT', 'ENDMARKER', 'INDENT', 'DEDENT', 'NEWLINE', 'ERRORTOKEN']
#     with tempfile.NamedTemporaryFile('w+t', suffix='.txt') as f:
#         f_file = open(f.name, 'w')
#         f_file.write(code_text)
#         f_file = open(f.name, 'r')
#         command = "python3 -m tokenize -e " + f.name
#         tokens = os.popen(command).readlines()
#         if len(tokens) == 0:
#             code_text = code_text.replace('\n', ' ')
#             code_text = re.sub(r'[\s]', '', code_text)
#             return code_text
#         for token in tokens:
#             print(token)
#             token = token.split()
#             if len(token) == 3:
#                 if token[1] in filter_token:
#                     continue
#                 code_str.append(eval(token[2]))
#         f_file.close()
#     return ''.join(code_str)


code_text = '''for i in range(10):
    print("a")
'''
# print(highlight_words(code_text))
print(lex_analysis(code_text))
# print(lex_analysis_char(code_text))

















