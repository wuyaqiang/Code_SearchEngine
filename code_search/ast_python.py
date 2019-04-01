#coding=utf-8
import ast
import tempfile

# py_file = open('./test_code/demo_py.txt', 'r')
# ast_root = ast.parse(py_file.read())

code_text = '''
a = (1,2,3,4)
'''

with tempfile.NamedTemporaryFile('w+t', suffix='.txt') as f:
    f_file = open(f.name, 'w')
    f_file.write(code_text)
    f_file = open(f.name, 'r')
    ast_root = ast.parse(f_file.read())


# for node in ast.walk(ast_root):
#     print(type(node).__name__)

def traverse_ast(node):
    for child in ast.iter_child_nodes(node):
        print(type(node).__name__, ' ——> ', type(child).__name__)
        traverse_ast(child)

# traverse_ast(ast_root)

def traverse_binary_tree(node):
    if node == None:
        return None
    print(node.value if node else 0, '——>', node.left.value if node.left else 0, 'and' , node.right.value if node.right else 0)
    traverse_binary_tree(node.left)
    traverse_binary_tree(node.right)

# def get_binary_tree_py(node):
#     if node == None:
#         return None
#     global code_str
#     word_combine = str(node.value if node else 0) + '_' + str(node.left.value if node.left else 0) +\
#                    '_' + str(node.right.value if node.right else 0)
#     code_str = code_str + ' ' + word_combine
#     get_binary_tree_py(node.left)
#     get_binary_tree_py(node.right)

def get_binary_tree_py(node):
    if node:
        word_combine = str(node.value if node else 0) + '_' + str(node.left.value if node.left else 0) +\
                       '_' + str(node.right.value if node.right else 0)
        return word_combine + ' ' + str(get_binary_tree_py(node.left)) + ' ' + str(get_binary_tree_py(node.right))

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

binary_root = convert_to_binary_py(ast_root)
traverse_binary_tree(binary_root)
code_str = ''
get_binary_tree_py(binary_root)
code_str = get_binary_tree_py(binary_root).replace(' None', '')
print(code_str)







