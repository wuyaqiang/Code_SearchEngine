#coding=utf-8
import os
import tempfile
import clang.cindex

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


def get_binary_tree_cpp(node):
    if node:
        word_combine = str(node.value if node else 0) + '_' + str(node.left.value if node.left else 0) +\
                       '_' + str(node.right.value if node.right else 0)
        return word_combine + ' ' + str(get_binary_tree_cpp(node.left)) + ' ' + str(get_binary_tree_cpp(node.right))

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


def convert_cpp(code_text):
    '''
    安装和运行clang参考以下两个链接：
    1. http://clang.llvm.org/get_started.html
    2. https://www.jianshu.com/p/cbb242026ff2
    '''
    try:
        # os.system("PYTHONPATH=/home/nlp/Clang/llvm/tools/clang/bindings/python")
        # os.system("export PYTHONPATH=/home/nlp/Clang/llvm/tools/clang/bindings/python")
        clang_path = os.path.abspath('./')
        clang.cindex.Config.set_library_path(clang_path + "/Clang/lib")
    except:
        pass

    with tempfile.NamedTemporaryFile('w+t', suffix='.txt') as f:
        f_file = open(f.name, 'w')
        f_file.write(code_text)
        f_file = open(f.name, 'r')
        index = clang.cindex.Index.create()
        tu = index.parse(f.name, ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])
        root = tu.cursor
    binary_root = convert_to_binary_cpp(root)
    code_str = get_binary_tree_cpp(binary_root).replace(' None', '')
    # code_str = get_binary_tree_cpp(binary_root).replace(' None', '').replace(' 0', '')

    return code_str


# code_text = '''
#  a = {1,2,3,4}
# '''
# print(len(convert_cpp(code_text).split()))
# print(convert_cpp(code_text).split())