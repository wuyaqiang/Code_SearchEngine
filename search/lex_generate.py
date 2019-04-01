#coding=utf-8
import time
import os
import pickle
import pymysql
from ChildProgramming.settings import BASE_DIR
from .code_processing.tokenize import tokenize

def code_list_generate():
    db_config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "db": "child_programming",
        "charset": "utf8"
    }
    my_db = pymysql.connect(**db_config)
    cursor = my_db.cursor()
    cursor.execute("SELECT id, code FROM problemCode")
    all_result = cursor.fetchall()

    id_list = []
    lex_list = []
    char_list = []
    for result in all_result:
        id_list.append(result[0])
        lex_list.append(lex_analysis(result[1]))
        char_list.append(lex_analysis_char(result[1]))

    root_path = BASE_DIR + '/search/code_processing/resource/'
    pickle.dump(lex_list, open(root_path + 'lex_list.txt', 'wb'))
    pickle.dump(char_list, open(root_path + 'char_list.txt', 'wb'))
    pickle.dump(id_list, open(root_path + 'id_list.txt', 'wb'))


if __name__ == '__main__':
    pass
    # time_1 = time.time()
    # code_list_generate()
    # print("time: ", time.time() - time_1)

    # db_config = {
    #     "host": "127.0.0.1",
    #     "port": 3306,
    #     "user": "root",
    #     "password": "123456",
    #     "db": "child_programming",
    #     "charset": "utf8"
    # }
    #
    # my_db = pymysql.connect(**db_config)
    #
    # cursor = my_db.cursor()

    # cursor.execute("SELECT code FROM problemCode WHERE language_id_id=1 ")
    # all_result_cpp = cursor.fetchall()
    # cpp_lex_list = []
    # cpp_char_list = []
    # for result in all_result_cpp:
    #     cpp_lex_list.append(lex_analysis(result[0]))
    #     cpp_char_list.append(lex_analysis_char(result[0]))
    # root_path = os.path.abspath('./')
    # pickle.dump(cpp_lex_list, open(root_path + '/code_processing/resource/cpp_lex_list.txt', 'wb'))
    # pickle.dump(cpp_char_list, open(root_path + '/code_processing/resource/cpp_char_list.txt', 'wb'))
    # cpp_lex_file = open(root_path + '/code_processing/resource/cpp_lex.txt', 'w')
    # cpp_lex_file.write('\n'.join(cpp_lex_list))
    # cpp_lex_file.close()
    # cpp_char_file = open(root_path + '/code_processing/resource/cpp_char.txt', 'w')
    # cpp_char_file.write('\n'.join(cpp_char_list))
    # cpp_char_file.close()
    #
    # cursor.execute("SELECT code FROM problemCode WHERE language_id_id=2 or language_id_id=3 ")
    # all_result_python = cursor.fetchall()
    # python_lex_list = []
    # python_char_list = []
    # for result in all_result_python:
    #     python_lex_list.append(lex_analysis(result[0]))
    #     python_char_list.append(lex_analysis_char(result[0]))
    # root_path = os.path.abspath('./')
    # pickle.dump(python_lex_list, open(root_path + '/code_processing/resource/python_lex_list.txt', 'wb'))
    # pickle.dump(python_char_list, open(root_path + '/code_processing/resource/python_char_list.txt', 'wb'))
    # python_lex_file = open(root_path + '/code_processing/resource/python_lex.txt', 'w')
    # python_lex_file.write('\n'.join(python_lex_list))
    # python_lex_file.close()
    # python_char_file = open(root_path + '/code_processing/resource/python_char.txt', 'w')
    # python_char_file.write('\n'.join(python_char_list))
    # python_char_file.close()

