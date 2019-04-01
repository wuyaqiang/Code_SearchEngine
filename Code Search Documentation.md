# 代码搜索引擎－详细文档

## 1. 概述

该模块的功能旨在进行相似代码的检索，即用户输入一个代码片段作为查询，系统从后台数据库返回与该查询相似性较高的代码，按相似度从高到低进行排列，展示给用户。

搜索引擎后台所采用的代码相似性匹配方法有三种，分别是原始字符串的精确匹配、词法分析后的Token串匹配、语法分析后的语法树相似性匹配。

下面我们先依次介绍三种匹配方式，然后再说明我们如何将三种方式的搜索结果进行结合。

##  2. 字符串精确匹配

该方法直接对源代码进行简单的预处理，然后进行字符串的**精确匹配**即可。

预处理过程如下：

将代码中的所有字符，根据附录中的“符号替换词典”进行替换，并加上“punc\_”前缀，所有字母组成的单词加上“char\_” 前缀，然后用空格隔开组成一个长字符串。例如：

> a = b + c     替换为：   char_a punc_BN char_b punc_BF char_c

注意：忽略了代码中的注释语句。

该方法处理样例如下：

源代码：

```python
# 这是一个注释
for i in range(10):
    print('abcde')
```

预处理后字符串：

```
char_for char_i char_in char_range punc_AW char_10 punc_AX punc_B0 char_print punc_AW punc_QT char_abcde punc_QT punc_AX
```

将查询代码和数据库中代码转换之后的字符串进行精确匹配，相同则返回，不同则不返回。



## 3. 词法分析 Token 串匹配

**词法分析**（**lexical analysis** ）是计算机科学中将字符序列转换为**标记**（token）序列的过程。

该方法对源代码进行词法分析，旨在忽略代码中变量名、数值大小这类区别。

进行词法分析的程序或者函数叫作**词法分析器**（lexical analyzer，简称 lexer）。

我们使用Python内置的词法分析器: [https://docs.python.org/3/library/tokenize.html](https://docs.python.org/3/library/tokenize.html).

可以直接使用指令：python3 -m tokenize -e  (+ filename) 对源代码进行词法分析，其中filename为代码文件所在路径。

我们对词法分析结果进行一些预处理，首先同样是将代码中的所有字符，根据附录中的“符号替换词典”进行替换，并加上“punc\_”前缀，然后将代码中的关键字统一加上“key\_”前缀，然后将词法分析中得到的Token标识符替换为较短的唯一标识符（根据附录中的”Token替换词典“，目的是使得最终得到的字符串长度较小）。例如：

> a = b + c 	替换为：  AO punc_BN AO punc_BF AO

> 注意： 词法分析将代码中的所有变量名标记为“NAME”，我们用“AO”缩写来进行表示。

该方法处理样例如下：

源代码：

```python
# 这是一个注释
for i in range(10):
    print('abcde')
```

处理后字符串：

```
key_for AO key_in key_range punc_AW AR punc_AX punc_B0 key_print punc_AW AU punc_AX
```

最后，将查询代码和数据库中代码转换之后的字符串进行精确匹配，相同则返回，不同则不返回。



## 4. 语法树相似性匹配

语法分析器基于特定语言的语法，将Token序列（由词法分析器生成）转换成一个抽象语法树。

抽象语法树（Abstract Syntax Tree，AST），或简称语法树（Syntax tree），是源代码语法结构的一种抽象表示。它以树状的形式表现编程语言的语法结构，树上的每个节点都表示源代码中的一种结构。之所以说语法是 “抽象” 的，是因为这里的语法并不会表示出真实语法中出现的每个细节。比如，嵌套括号被隐含在树的结构中，并没有以节点的形式呈现。

具体概念请参考维基百科[抽象语法树](https://www.wikiwand.com/zh-hans/%E6%8A%BD%E8%B1%A1%E8%AA%9E%E6%B3%95%E6%A8%B9)，以及其他相关资料。

以下是表达式 2 × 7 + 3, 转换成语法树的例子：

![](https://ruslanspivak.com/lsbasi-part7/lsbasi_part7_ast_01.png)

在进行语法分析时，我们采用的工具如下：

1. Python ast : Python自带的语法分析器模块，通过parse()函数生成抽象语法树，并提供对抽象语法树的遍历。链接如下：[https://docs.python.org/3.7/library/ast.html](https://docs.python.org/3.7/library/ast.html).
2. C++ Clang : 提供了C、C++等语言的语法分析器。链接如下：[https://clang.llvm.org/](https://clang.llvm.org/).

在进行语法分析得到语法树之后，我们采用论文[ Similarity Evaluation on Tree-structured Data ](https://cloud.kaust.edu.sa/Documents/sigmod05.pdf)中提出的方法进行语法树的特征提取，将树的表达转化成为一个字符序列。转换方法如下：

1. 先将语法树转换成二叉树，采用左孩子右兄弟的转换方法
2. 我们对二叉树的所有叶结点进行结点填充，使得每个叶节点都拥有其左孩子和右孩子结点
3. 取出转换之后二叉树中的每个两层子树，当做一个特征，将该两层子树结构中的三个结点值用下划线“\_”连接起来，作为最终树的字符串表达中的一项
4. 将该语法树中的所有特征项用空格隔开，作为最终的树的字符串表达

![]()



## 5. 检索方案结合



## 附录

###  1. 符号替换对应词典

```python
{
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
```

###  2. Token 替换词典

```python
{
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
```