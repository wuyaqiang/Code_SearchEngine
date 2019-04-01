#coding=utf-8
import ast
import os
import sys
import tempfile
import logging
from lib2to3.main import main

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
        self.value = type(node).__name__
        for child in ast.iter_child_nodes(node):
            self.childs.append(child)
            self.child_num += 1

def get_binary_tree_py(node):
    if node:
        word_combine = str(node.value if node else 0) + '_' + str(node.left.value if node.left else 0) +\
                       '_' + str(node.right.value if node.right else 0)
        return word_combine + ' ' + str(get_binary_tree_py(node.left)) + ' ' + str(get_binary_tree_py(node.right))

def convert_to_binary_py(root):
    '''将多叉树转化成二叉树(左孩子右兄弟表达)'''
    if root == None:
        return None
    node = TreeNode(root)
    binary_root = BinaryTreeNode(node.value)
    binary_root.left = convert_to_binary_py(node.childs[0] if len(node.childs)>0 else None)
    brother = binary_root.left
    for i in range(1,node.child_num):
        brother.right = convert_to_binary_py(node.childs[i] if len(node.childs)>0 else None)
        brother = brother.right
    return binary_root

def traverse_binary_tree(node):
    if node == None:
        return None
    print(node.value if node else 0, '——>', node.left.value if node.left else 0, 'and' , node.right.value if node.right else 0)
    traverse_binary_tree(node.left)
    traverse_binary_tree(node.right)

def convert_python(code_text):
    # try:
    #     code_text = convert_to_py3(code_text)
    # except:
    #     code_text = code_text

    ast_root = ast.parse(code_text)

    binary_root = convert_to_binary_py(ast_root)
    code_str = get_binary_tree_py(binary_root).replace(' None', '')

    return code_str
