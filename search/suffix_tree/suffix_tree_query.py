#coding=utf-8
import os
import sys
import time
import shelve
from suffix_trees import STree
sys.setrecursionlimit(100000)

def deal_search_result(result):
    search_kv = {}
    search_result = [x for list in result for x in list]
    for i in search_result:
        if str(i) not in search_kv:
            search_kv[str(i)] = 1
        else:
            search_kv[str(i)] += 1
    search_kv = sorted(search_kv.items(), key=lambda e:e[1], reverse=True)
    return search_kv

def deal_N_search_result(search_result):
    search_kv = {}
    for i in search_result:
        if str(i) not in search_kv:
            search_kv[str(i)] = 1
        else:
            search_kv[str(i)] += 1
    search_kv = sorted(search_kv.items(), key=lambda e:e[1], reverse=True)
    return search_kv

def stree_Deserialization(stree_path):

    strees = []
    start = time.time()
    streesDB = shelve.open(stree_path)
    N = len(streesDB)
    print('length of streesDB: ', N)

    print('Reading Suffix Tree...')
    for i in range(N):
        strees.append(streesDB[str(i)])
    print('Read Time: ',time.time()-start)
    print('length of strees: ', len(strees))
    print(strees[-1])
    return strees

def stree_Search(string, stree):

    search_result = []
    start = time.time()
    if type(stree) != type([]):
        search_result = deal_search_result(stree.find_all(string))
    elif type(stree) == type([]):
        length = len(stree)
        # print('length:',length)
        cut_point = stree[length-1]
        print('cut_point: ', cut_point)
        N = length-1
        for i in range( N ):
            search_result.append( [(x + i * cut_point) for list in stree[i].find_all(string) for x in list] )
        search_result = deal_search_result(search_result)
    else:
        print('Type Error!')
    print('Search Time: ',time.time()-start)
    return search_result


# root_path = os.path.abspath('./')
# lex_char_st = root_path + '/code_processing/resource/lex_char_st.db'
# lex_st = root_path + '/code_processing/resource/lex_st.db'
# char_suffix_tree = stree_Deserialization(lex_char_st)
# lex_suffix_tree = stree_Deserialization(lex_st)
#
# while True:
#     print('Please Input Query Code: ')
#     string = input()
#     # one_search_result = stree_Search(string = string,stree=one_lex_char_st)
#     char_search_result = stree_Search(string = string, stree = char_suffix_tree)
#     lex_search_result = stree_Search(string = string, stree = lex_suffix_tree)
#     print('char Query Result: ', len(char_search_result))
#     print(char_search_result)
#     print('lex Query Result: ', len(lex_search_result))
#     print(lex_search_result)