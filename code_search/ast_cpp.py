#coding=utf-8

import sys
import os
import tempfile
import clang.cindex

'''
在Python中执行终端命令有以下两种方法：
1. os.system("命令")   这个方法得不到 shell 命令的输出。
2. os.popen("命令").read()    这个方法能得到命令执行后的结果是一个字符串，要自行处理才能得到想要的信息。
'''

# os.system("PYTHONPATH=/home/wuyaqiang/Clang/llvm/tools/clang/bindings/python")
# os.system("export PYTHONPATH=/home/wuyaqiang/Clang/llvm/tools/clang/bindings/python")

clang.cindex.Config.set_library_path("/home/wuyaqiang/myprojects/CodeSearchEngine/ChildProgramming/Clang/lib")

def show_token(node):
    tokens = node.get_tokens()
    for t in tokens:
        print(t.spelling)

def traverse(node):
    # print(node.kind)
    for child in node.get_children():
        print(node.kind.name, ' ——> ', child.kind.name)
        traverse(child)

count = 0
def traverse_binary_tree(node):
    global count
    count += 1
    if node == None:
        return None
    print(node.value if node else 0, '——>', node.left.value if node.left else 0, 'and' , node.right.value if node.right else 0)
    traverse_binary_tree(node.left)
    traverse_binary_tree(node.right)

# def get_binary_tree_cpp(node):
#     if node == None:
#         return None
#     global code_str
#     word_combine = str(node.value if node else 0) + '_' + str(node.left.value if node.left else 0) +\
#                    '_' + str(node.right.value if node.right else 0)
#     code_str = code_str + ' ' + word_combine
#     get_binary_tree_cpp(node.left)
#     get_binary_tree_cpp(node.right)

def get_binary_tree_cpp(node):
    if node:
        word_combine = str(node.value if node else 0) + '_' + str(node.left.value if node.left else 0) +\
                       '_' + str(node.right.value if node.right else 0)
        return word_combine + ' ' + str(get_binary_tree_cpp(node.left)) + ' ' + str(get_binary_tree_cpp(node.right))


code_text = '''
int n[ 10 ];
'''

with tempfile.NamedTemporaryFile('w+t', suffix='.txt') as f:
    f_file = open(f.name, 'w')
    f_file.write(code_text)
    f_file = open(f.name, 'r')
    index = clang.cindex.Index.create()
    tu = index.parse(f.name, ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])
    root = tu.cursor

# index = clang.cindex.Index.create()
# tu = index.parse("./test_code/demo_cpp.txt", ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])
# show_token(tu.cursor)
# root = tu.cursor    # get the root of AST
# traverse(root)

# ast_tree = os.popen("clang -Xclang -ast-dump -fsyntax-only ./test_code/demo_cpp.txt").read()     # 使用clang命令得到ast

class BinaryTreeNode:
    '''转化之后的二叉树中的树结点'''
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

class TreeNode:
    '''原始多叉树中的树结点'''
    def __init__(self, node):
        self.childs = []
        self.child_num = 0
        self.value = node.kind.name
        for child in node.get_children():
            self.childs.append(child)
            self.child_num += 1

def convert_to_binary_cpp(root):
    '''将多叉树转化成二叉树(左孩子右兄弟表达)'''
    if root:
        node = TreeNode(root)
        binary_root = BinaryTreeNode(node.value)
        binary_root.left = convert_to_binary_cpp(node.childs[0] if len(node.childs)>0 else None)
        brother = binary_root.left
        for i in range(1,node.child_num):
            brother.right = convert_to_binary_cpp(node.childs[i] if len(node.childs)>0 else None)
            brother = brother.right
        return binary_root
    return root

# binary_root = convert_to_binary_cpp(root)
# traverse_binary_tree(binary_root)

# print('sladjfashdfloia: ', count)
# code_str = ''
# get_binary_tree_cpp(binary_root)
# code_str = get_binary_tree_cpp(binary_root).replace(' None', '')
# print(len(code_str))