#coding=utf-8
import time
import os
import sys
import pickle
from suffix_trees import STree
import shelve

sys.setrecursionlimit(100000)

def build_One_STree(text):
    '''
    将所有text建立一棵树, 此时树过大, 无法存入磁盘文件
    '''
    start = time.time()
    st = STree.STree(text)
    print('Build Tree Total Time: ',time.time()-start)
    return st

def build_N_STree(text,cut_point=30):
    N = len(text) // cut_point if len(text) % cut_point == 0 else len(text) // cut_point + 1
    strees = []
    start = time.time()
    for i in range(N):
        if i >= N-1:
            new_text = text[cut_point * i : ]
            # print('最后一个树的文档数量:',len(new_text))
        else:
            new_text = text[cut_point * i : cut_point * i + cut_point]
        strees.append(STree.STree(new_text))
    strees.append(cut_point)
    # print('STrees Number: ', len(strees))
    print('Build %d Trees, ' %N, 'Total Build Time: ',time.time()-start)
    return strees

def stree_Serialization(stree, trees_path):

    N = len(stree)
    print('N大小: ', N)
    sts = shelve.open(trees_path)
    try:
        for i in range(N-1):
            print(i)
            sts[str(i)] = stree[i]
        sts[str(N-1)] = stree[N-1]
        print('str(N-1): ', str(N-1))
        print('stree[N-1]: ', stree[N-1])
        print('STree Number: ',len(sts))
    except:
        print('Something Error In Serialization!')
    finally:
        sts.close()

def st_generate_serialize(text_list_path, st_save_path):
    with open(text_list_path, 'rb') as f:
        text = pickle.load(file=f)
    N_suffix_tree = build_N_STree(text)
    stree_Serialization(N_suffix_tree, st_save_path)

def st_generation(text_list_path):
    with open(text_list_path, 'rb') as f:
        text = pickle.load(file=f)
    print('Code Number: ', len(text))

    N_suffix_tree = build_N_STree(text[:1000])

    return N_suffix_tree


# if __name__ == '__main__':
#
#     root_path = os.path.abspath('../')
#     # lex_char_path = root_path + '/code_processing/resource/lex_char_list.txt'
#     # lex_path = root_path + '/code_processing/resource/lex_list.txt'
#     # lex_char_st_path = root_path + '/code_processing/resource/lex_char_st.db'
#     # lex_st_path = root_path + '/code_processing/resource/lex_st.db'
#     cpp_char_path = root_path + '/code_processing/resource/cpp_char_list.txt'
#     cpp_lex_path = root_path + '/code_processing/resource/cpp_lex_list.txt'
#     python_char_path = root_path + '/code_processing/resource/python_char_list.txt'
#     python_lex_path = root_path + '/code_processing/resource/python_lex_list.txt'
#     cpp_char_st_path = root_path + '/code_processing/resource/cpp_char_st.db'
#     cpp_lex_st_path = root_path + '/code_processing/resource/cpp_lex_st.db'
#     python_char_st_path = root_path + '/code_processing/resource/python_char_st.db'
#     python_lex_st_path = root_path + '/code_processing/resource/python_lex_st.db'
#
#     st_generate_serialize(cpp_char_path, cpp_char_st_path)
#     st_generate_serialize(cpp_lex_path, cpp_lex_st_path)
#     st_generate_serialize(python_char_path, python_char_st_path)
#     st_generate_serialize(python_lex_path, python_lex_st_path)