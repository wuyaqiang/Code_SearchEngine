# -*-coding:utf-8 -*-
__author__ = '$'

import math
from search import models
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from haystack.query import SQ, SearchQuerySet, EmptySearchQuerySet
from .models import Problem, Question, Label, ProblemCode
import operator
import json
import re
from rest_framework import serializers
from haystack.inputs import Raw,AutoQuery,Exact

class Label_tree(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = ('id','label_name','father_id')



def problem_search(request):
    return render(request, 'search/search_test.html')


def result_search(request):

    if request.GET['q']:
        qq = request.GET['q']
        posts = SearchQuerySet().models(Problem).all()
        posts = SearchQuerySet().filter(content=qq)
        return render(request, 'search/search.html', {'query': qq})
    else:
        return HttpResponse('搜索框内容为空!')


def mysearch(request):  # 全文搜索

    query = request.GET['q']
    # posts = SearchQuerySet().models(Problem).all()
    if query == '':
        posts = SearchQuerySet().using('problem').models(Problem).all()
        # posts = SearchQuerySet().models(Problem).filter(id=2968)
        # posts = SearchQuerySet().filter(id=997)
    else:
        posts = SearchQuerySet().using('problem').models(Problem).filter(content=query)

    # print('索引：',len(posts))
    # pp = SearchQuerySet().models(Problem).all()
    # print('索引：',len(pp))

    # rr = Problem.objects.all()
    # print('数据库：',len(rr))


    # 找条件
    condition_now = {}
    for i in posts:
        # rr = Problem.objects.filter(id=i.id).first()
        # print('rr_id:',rr.id)
        # for kk in rr.label.all():
        #     print('label_name:',kk.label_name)
        # print('value:',i.value)
        for j in i.label:
            # print(j)
            if j != '':
                if not condition_now.get(j):
                    condition_now.update({j: 1})
                else:
                    k = condition_now[j] + 1
                    condition_now.update({j: k})
    kw = sorted(condition_now.items(), key=operator.itemgetter(1), reverse=True)
    # print(condition_now)

    keywords = []
    for i in posts:
        res = []
        for k in i.label:
            res.append(k)
        keywords.append(res)

    result_num = posts.count()
    posts = zip(posts, keywords)

    data = Label_tree(Label.objects.all(), many=True).data
    dict_tree = []
    for i in data:
        for j in kw:
            if i['label_name'] == j[0]:
                dict_tree.append(dict(
                    [('id', i['id']), ('label_name', i['label_name'] + '-' + str(j[1])), ('father_id', i['father_id']),
                     ('num', j[1])]))

    return render(request, 'search/search_result.html',
                  {'posts': posts, 'query_title': query, 'query_describe': query, 'query_keywords': query,
                   'query_difficulty': query, 'query': query,
                   'result_num': result_num, 'kw': kw, 'data': json.dumps(dict_tree)})
def mysearch_other(request):  # 高级搜索

    posts = SearchQuerySet().using('problem').models(Problem).all()

    label_con = []
    title=''
    description=''
#  开始处理筛选条件
    for i in request.GET.lists():
        if 'label_con' in i[0] :
            labels = request.GET['label_con'].strip()
            if labels!='':
                label_con = labels.strip().split('|')
            break
    for i in request.GET.lists():
        if 'delete_label' in i[0] :
            delete_label = request.GET['delete_label'].strip()
            if delete_label!='':
                label_con.remove(delete_label)
            break
#  结束处理筛选条件

    query_difficulty = []
    for e in request.GET.lists():
        if e[0]=='difficulty' and len(e[1])!=0:

            for i in range(len(e[1])):   # 对于一类条件下的多个选项
                if e[1][i] != '':
                    query_difficulty.append(e[1][i])
                    posts = posts.filter_or(difficulty=e[1][i])

            continue
        if e[0]=='label' and len(e[1])!=0:
            for i in range(len(e[1])):

                if e[1][i] not in label_con:
                    label_con.append(e[1][i])
    label_con_string = '|'.join(label_con)
    for i in label_con:
        posts = posts.filter_or(label=i)

    for i in request.GET.lists():
        if 'title' in i[0]:
            title = request.GET['title'].strip()
            if title != '':
                posts = posts.filter_and(title=title.strip())
            break
    for i in request.GET.lists():
        if 'description' in i[0]:
            description = request.GET['description'].strip()
            if description!='':
                posts = posts.filter_and(description=description.strip())
            break

    condition_now = {}
    for i in posts:
        for j in i.label:
            if j != '' and j not in label_con:
                if  not  condition_now.get(j):
                    condition_now.update({j: 1})
                else:
                    k = condition_now[j] + 1
                    condition_now.update({j: k})
    kw = sorted(condition_now.items(),key=operator.itemgetter(1),reverse=True)

    keywords =[]
    for i in posts:
        res = []
        for k in i.label:
            res.append(k)
        keywords.append(res)
    result_num = posts.count()
    posts = zip(posts,keywords)

    data = Label_tree(Label.objects.all(), many=True).data
    dict_tree = []
    for i in data:
        for j in kw:
            if i['label_name']==j[0]:
                dict_tree.append(dict([('id',i['id']),('label_name',i['label_name']+'-'+str(j[1])),('father_id',i['father_id']),('num',j[1])]))

    return render(request, 'search/search_result.html', {'posts':posts, 'query_title':title, 'query_describe':description, 'query_keywords':' '.join(label_con), 'query_difficulty':' '.join(query_difficulty),'query': ''
                            ,'result_num':result_num,'kw':kw,'label_con':label_con,'label_con_string':label_con_string,'data':json.dumps(dict_tree)})
def problem_detail(request,problem_id):   # 点击搜索结果，展示具体的问题
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request, "oj/problem_detail.html", {"problem": problem})

def find_question(request):

    return render(request, 'search/find_question.html')

def question_answer(request):

    return render(request, 'search/find_answer.html')

def question_result(request):
    query = request.GET['q'].strip()
    if query == '':
        posts = SearchQuerySet().using('question').models(Question).all()
    else:
        posts = SearchQuerySet().using('question').models(Question).filter(content = query)

    result_num = posts.count()

    return render(request, 'search/search_anwser.html',
                  {'posts': posts, 'query_title': query, 'query_describe': query, 'query_keywords': query,
                   'query': query
                      , 'result_num': result_num})

def question_detail(request,question_id):

    post = Question.objects.filter(id=question_id)


    return render(request, 'search/show_question.html', {'post': post})



'''wuyaqiang'''
import os
import time
import pickle
from django.db.models import Case, When
from ChildProgramming.settings import BASE_DIR
from .code_processing.ast_python import convert_python
from .code_processing.ast_cpp import convert_cpp
from .code_processing.code_utility import cpp_head_remove, cpp_head_convert
from .code_processing.tokenize import highlight_words, tokenize
from .suffix_tree.suffix_tree_query import stree_Deserialization, stree_Search

def code_search(request):  # 代码搜索

    all_time = time.time()

    query = request.GET['code1']
    # query_language = request.GET['select_language']
    raw_query = query
    query_highlight_token = highlight_words(raw_query)

    all_posts = []
    all_posts_id = []
    all_posts_filtered = []

    if query != "":
        print('Query Code: ', query)
        lex_token = tokenize(raw_query, "lex").strip()
        char_token = tokenize(raw_query, "char").strip()
        print('Lex Tokens: ', lex_token)
        print('Char Tokens: ', char_token)
        time_1 = time.time()

        if char_token == "":
            char_search_result = []
        else:
            char_search_result = SearchQuerySet().using('problemcode').filter(content=Exact(char_token))
            # char_search_result = SearchQuerySet().using('problemcode').all()
            # for query_item in char_token.split():
            #     char_search_result = char_search_result.filter_or(content=query_item)
            # char_search_result = list(char_search_result)
        for item in char_search_result[:2000]:
            id = item.id
            all_posts.append(item)
            all_posts_id.append(id)
        char_search_num = len(char_search_result)
        print(all_posts_id[:10])
        print('char search result num: ', char_search_num)

        if lex_token == "":
            lex_search_result = []
        else:
            lex_search_result = SearchQuerySet().using('problemcode').filter(content=Exact(lex_token))
            # lex_search_result = SearchQuerySet().using('problemcode').all()
            # for query_item in lex_token.split():
            #     lex_search_result = lex_search_result.filter_or(content=query_item)
            # lex_search_result = list(lex_search_result)
        for item in lex_search_result[:2000]:
            id = item.id
            if id not in all_posts_id:
                all_posts.append(item)
                all_posts_id.append(id)
        lex_search_num = len(lex_search_result)
        print(all_posts_id[:10])
        print('lex search result num: ', lex_search_num)

        print('time_1: ', time.time()-time_1)
        time_2 = time.time()

        if len(query_highlight_token.split()) == 1:
            # 如果查询代码太短(只包含一个word), 则直接跳过语法分析搜索过程
            posts_python_ast = []
            python_search_num = 0
            posts_cpp_ast = []
            cpp_search_num = 0
            print('Too Short To AST Analysis.')
        else:
            # 进行python语法分析, 并根据语法结果找到相似代码, 追加在lex_posts和char_posts后面:
            try:
                query_ast = convert_python(raw_query)
                print('Python Query AST: ', query_ast)
                query_ast = query_ast.split()
                if len(query_ast) == 1:
                    posts_python_ast = []
                else:
                    posts_python_ast = SearchQuerySet().using('problemcode').all()
                    for query_item in query_ast:
                        posts_python_ast = posts_python_ast.filter_or(content=query_item)
                python_search_num = len(posts_python_ast)
                print('python search result num: ', python_search_num)
                # posts_ast = posts_ast[:1000]
                # posts = posts | posts_python_ast
                # char_lex_id = set(char_result_id + lex_result_id)
                # posts += [post for post in posts_ast if post.id not in char_lex_id]
                # python_ast_id = [int(post.id) for post in posts_ast]
            except:
                posts_python_ast = []
                python_search_num = 0
                print('Python AST Analysis Failed.')

            # 进行C++语法分析, 并根据语法结果找到相似代码, 追加在lex_posts和char_posts后面:
            try:
                query_ast = convert_cpp(cpp_head_remove(raw_query))
                print('C++ Query AST: ', query_ast)
                query_ast = query_ast.split()
                if len(query_ast) == 1:
                    posts_cpp_ast = []
                else:
                    posts_cpp_ast = SearchQuerySet().using('problemcode').all()
                    for query_item in query_ast:
                        posts_cpp_ast = posts_cpp_ast.filter_or(content=query_item)
                cpp_search_num = len(posts_cpp_ast)
                print('c++ search result num: ', cpp_search_num)
                # posts_ast = posts_ast[:1000]
                # posts = posts | posts_cpp_ast
                # 已经存在的post_id, 即char, lex, python的并集:
                # char_lex_python_id = set(char_result_id + lex_result_id + python_ast_id)
                # posts += [post for post in posts_ast if post.id not in char_lex_python_id]
            except:
                posts_cpp_ast = []
                cpp_search_num = 0
                print('C++ AST Analysis Failed.')

        for item in posts_python_ast[:2000]:
            id = item.id
            if id not in all_posts_id:
                all_posts.append(item)
                all_posts_id.append(id)
        for item in posts_cpp_ast[:2000]:
            id = item.id
            if id not in all_posts_id:
                all_posts.append(item)
                all_posts_id.append(id)

        all_posts_num = len(all_posts)
        print('All Posts Num: ', all_posts_num)
        print('time_2: ', time.time() - time_2)

        time_3 = time.time()
        for item in all_posts:
            if Problem.objects.filter(id=item.problem).exists():
                item.code = cpp_head_convert(item.code)
                all_posts_filtered.append(item)
        print('time_3: ', time.time()-time_3)

    result_num = len(all_posts_filtered)
    print('Returned Posts Count: ', result_num)

    print('all_time: ', time.time()-all_time)

    return render(request, 'search/code_search_result.html',
                  {'posts': all_posts_filtered, 'raw_query': raw_query, 'query_token': query_highlight_token,
                   'result_num': result_num})


'''--------------------------------------------------------------------------------------------------------------'''

def api_code_search(request, search_way=1):

    query = request.POST['title']
    language = {
        1: "cpp",
        2: "python"
    }
    query_language = language[int(request.POST['queryLanguage'])]
    raw_query = query
    query_token = highlight_words(raw_query)
    highlight_dict = {}
    for word in query_token.split(" "):
        if word not in highlight_dict and word.strip() != "":
            highlight_dict[word] = "<font>" + word + "</font>"

    try:
        posts = []
        if query == '':
            posts = SearchQuerySet().using('problemcode').all()
        else:
            print('Query Code: ', query)
            if query_language == 'python':
                py_lex_token = lex_analysis(raw_query)
                py_char_token = lex_analysis_char(raw_query)
                # print('py_lex_token: ', py_lex_token)
                # print('py_char_token: ', py_char_token)
                try:
                    lex_search_result = stree_Search(string=py_lex_token, stree=lex_suffix_tree)
                    char_search_result = stree_Search(string=py_char_token, stree=char_suffix_tree)
                    print('Lex Result: ', len(lex_search_result))
                    print('Char Result: ', len(char_search_result))
                    lex_result_id = []
                    char_result_id = []
                    for item in lex_search_result:
                        lex_result_id.append(int(item[0]) + 2)
                    for item in char_search_result:
                        char_result_id.append(int(item[0]) + 2)
                    # print('Lex Result ID: ', lex_result_id)
                    # print('Char Result ID: ', char_result_id)
                    problem_code_lex_obj = ProblemCode.objects.filter(id__in=lex_result_id)
                    problem_code_char_obj = ProblemCode.objects.filter(id__in=char_result_id)
                    problem_code_lex_obj = dict([(obj.id, obj) for obj in problem_code_lex_obj])
                    problem_code_char_obj = dict([(obj.id, obj) for obj in problem_code_char_obj])
                    posts = []
                    for id in char_result_id:
                        if problem_code_char_obj[id].language_id_id == 1:  # 过滤掉搜索结果中的所有C++代码，只列出Python代码
                            continue
                        posts.append(problem_code_char_obj[id])
                    for id in lex_result_id:
                        # 将lex_posts追加在char_posts后面, 如果在char_posts里已经存在, 就不再追加.
                        if problem_code_lex_obj[id].language_id_id == 1:
                            continue
                        if id in char_result_id:
                            continue
                        if len(list(set(query_token.split()).intersection(
                                set(highlight_words(problem_code_lex_obj[id].code).split())))) == 0:
                            continue
                        posts.append(problem_code_lex_obj[id])
                    try:
                        query_ast = convert_python(raw_query)
                        # print('Query AST: ', query_ast)
                        query_ast = query_ast.split()
                        posts_ast = SearchQuerySet().using('problemcode').all()
                        for query_item in query_ast:
                            posts_ast = posts_ast.filter_or(content=query_item)
                        for post in posts_ast:
                            if post.language == 1:
                                continue
                            if len(list(set(query_token.split()).intersection(
                                    set(highlight_words(post.code).split())))) == 0:
                                continue
                            if int(post.id) in char_result_id or post.id in lex_result_id:
                                continue
                            posts.append(post)
                    except:
                        print('AST Analysis Failed.')
                except:
                    posts = []

            if query_language == 'cpp':
                cpp_lex_token = lex_analysis(raw_query)
                cpp_char_token = lex_analysis_char(raw_query)
                # print('cpp_lex_token: ', cpp_lex_token)
                # print('cpp_char_token: ', cpp_char_token)
                try:
                    lex_search_result = stree_Search(string=cpp_lex_token, stree=lex_suffix_tree)
                    char_search_result = stree_Search(string=cpp_char_token, stree=char_suffix_tree)
                    # print('Lex Result: ', lex_search_result)
                    # print('Char Result: ', char_search_result)
                    lex_result_id = []
                    char_result_id = []
                    for item in lex_search_result:
                        lex_result_id.append(int(item[0]) + 2)
                    for item in char_search_result:
                        char_result_id.append(int(item[0]) + 2)
                    # print('Lex Result ID: ', lex_result_id)
                    # print('Char Result ID: ', char_result_id)
                    problem_code_lex_obj = ProblemCode.objects.filter(id__in=lex_result_id)
                    problem_code_char_obj = ProblemCode.objects.filter(id__in=char_result_id)
                    problem_code_lex_obj = dict([(obj.id, obj) for obj in problem_code_lex_obj])
                    problem_code_char_obj = dict([(obj.id, obj) for obj in problem_code_char_obj])
                    posts = []
                    for id in char_result_id:
                        if problem_code_char_obj[id].language_id_id == 2 or problem_code_char_obj[
                            id].language_id_id == 3:
                            # 过滤掉搜索结果中的所有Python代码，只列出C++代码
                            continue
                        problem_code_char_obj[id].code = cpp_head_convert(problem_code_char_obj[id].code)
                        posts.append(problem_code_char_obj[id])
                    for id in lex_result_id:
                        # 将lex_posts追加在char_posts后面, 如果在char_posts里已经存在, 就不再追加.
                        if problem_code_lex_obj[id].language_id_id == 2 or problem_code_lex_obj[id].language_id_id == 3:
                            continue
                        if id in char_result_id:
                            continue
                        if len(list(set(query_token.split()).intersection(
                                set(highlight_words(problem_code_lex_obj[id].code).split())))) == 0:
                            continue
                        problem_code_lex_obj[id].code = cpp_head_convert(problem_code_lex_obj[id].code)
                        posts.append(problem_code_lex_obj[id])
                    try:
                        query_ast = convert_cpp(cpp_head_remove(raw_query))
                        # print('Query AST: ', query_ast)
                        query_ast = query_ast.split()
                        posts_ast = SearchQuerySet().using('problemcode').all()
                        for query_item in query_ast:
                            posts_ast = posts_ast.filter_or(content=query_item)
                        for post in posts_ast:
                            if post.language == 2 or post.language == 3:
                                continue
                            if len(list(set(query_token.split()).intersection(
                                    set(highlight_words(post.code).split())))) == 0:
                                continue
                            if int(post.id) in char_result_id or post.id in lex_result_id:
                                continue
                            post.code = cpp_head_convert(post.code)
                            posts.append(post)
                    except:
                        print('AST Analysis Failed.')
                except:
                    posts = []

        posts_id = []
        for post in posts:
            posts_id.append(post.problem_id_id)
        problem_obj = Problem.objects.all().filter(id__in=posts_id)
        problem_obj = dict([(obj.id, obj) for obj in problem_obj])
        pro_obj = []
        for id in posts_id:
            try:
                pro_obj.append(problem_obj[int(id)])
            except:
                continue
    except:
        pro_obj = []
        posts = []

    posts = list(zip(posts, pro_obj))
    result_num = len(pro_obj)
    print('Returned Posts Count: ', result_num)

    if search_way == 0:
        return posts

    json_dict = {}
    json_dict['code'] = 0
    json_dict['msg'] = "操作成功"
    page_info = {}
    pageNum = int(request.POST["pageNum"])
    pageSize = int(request.POST["pageSize"])
    page_info['pageNums'] = pageNum
    page_info['pageSize'] = pageSize
    total_page = math.ceil(result_num / pageSize)
    page_info['pageTotal'] = total_page
    page_info['pageCount'] = result_num
    json_dict['pageInfo'] = page_info
    if pageNum == total_page:
        returned_posts = posts[(pageNum - 1) * pageSize : ]
    else:
        returned_posts = posts[(pageNum - 1) * pageSize : pageNum * pageSize]
    data = []
    for item in returned_posts:
        item_dict = {}
        item_dict['id'] = item[1].id

        item_dict['contentType'] = request.POST['menuType']

        # 将代码中需要高亮的部分用<font></font>标签标注起来
        for word, replace_word in highlight_dict.items():
            item[0].code = item[0].code.replace(word, replace_word)

        item_info = {}
        item_info['title'] = item[1].title
        item_info['sourceName'] = item[1].source
        item_info['createTime'] = str(item[1].create_time)
        item_info['level'] = item[1].difficulty
        item_info['labels'] = ""
        item_info['ansName'] = ""
        item_info['content'] = item[0].code
        item_info['readNum'] = ""
        item_info['praiseNum'] = ""
        item_info['status'] = ""
        item_info['imgUrl'] = ""
        item_info['answersNums'] = ""
        item_info['language'] = ""
        item_info['languageCode'] = ""

        item_dict['info'] = item_info
        data.append(item_dict)
    json_dict['data'] = data

    return json_dict

def api_mysearch_other(request, search_way=1):
        pageNum = int(request.POST['pageNum'].strip())
        pageSize = int(request.POST['pageSize'].strip())

        title = request.POST['title'].strip()
        query = title.split(' ')

        # print(query)

        level = int(request.POST['level'].strip())
        labelType = int(request.POST['labelType'].strip())
        posts = SearchQuerySet().using('problem').models(Problem).filter_and(content=title)
        if level != 0:
            posts = posts.filter_and(difficulty=level)
        if labelType != 0:
            posts = posts.filter_and(labels=labelType)

        if search_way == 0:
            return posts

        result_num = len(posts)

        # 每页显示条数
        json_dict = {}
        json_dict['code'] = 0
        json_dict['msg'] = "操作成功"
        page_info = {}
        page_info['pageNums'] = pageNum
        page_info['pageSize'] = pageSize
        total_page = math.ceil(result_num/pageSize)
        page_info['pageTotal'] = total_page
        page_info['pageCount'] = result_num
        json_dict['pageInfo'] = page_info
        if pageNum == total_page:
            returned_posts = posts[(pageNum - 1) * pageSize :]
        else:
            returned_posts = posts[
                             (pageNum - 1) * pageSize : pageNum * pageSize]
        data = []
        for item in returned_posts:
            item_dict = {}
            item_dict['id'] = item.id
            item_dict['contentType'] = 2

            item_info = {}
            labels = []
            for la in item.label:
                labels.append(la)
            item_labels = ','.join(labels)
            item_title = item.title
            item_description = item.description
            for Q in query:
                if item_title.lower().find(Q.lower())>-1:
                    # print(1)
                    pos = re.finditer(Q.lower(),item_title.lower())
                    for pp in pos:
                        # print(item.id,pp.start())
                        length = len(Q)
                        # print(length)
                        res = item_title[pp.start():pp.start()+length]
                    Q_r = '<font>' + res + '</font>'
                    item_title = item_title.replace(res, Q_r)
                else:
                    # print('0000')
                    res = Q
                    Q_r = '<font>' + res + '</font>'
                    item_title = item_title.replace(res,Q_r)

                if item_description.lower().find(Q.lower())>-1:
                    # print(1)

                    pos = re.finditer(Q.lower(),item_description.lower())
                    for pp in pos:
                        # print(item.id,pp.start())
                        length = len(Q)
                        # print(length)
                        res = item_description[pp.start():pp.start()+length]
                    Q_r = '<font>' + res + '</font>'
                    item_description = item_description.replace(res, Q_r)
                else:
                    # print('0000')
                    res = Q
                    Q_r = '<font>' + res + '</font>'
                    item_description = item_description.replace(res,Q_r)

                if item_labels.lower().find(Q.lower())>-1:
                    # print(1)
                    pos = re.finditer(Q.lower(),item_labels.lower())
                    for pp in pos:
                        # print(item.id,pp.start())
                        length = len(Q)
                        # print(length)
                        res = item_labels[pp.start():pp.start()+length]
                    Q_r = '<font>' + res + '</font>'
                    item_labels = item_labels.replace(res, Q_r)
                else:
                    # print('0000')
                    res = Q
                    Q_r = '<font>' + res + '</font>'
                    item_labels = item_labels.replace(res,Q_r)


            item_info['title'] = item_title
            item_info['content'] = item_description
            item_info['labels'] = item_labels

            item_info['sourceName'] = item.source
            item_info['createTime'] = item.create_time
            item_info['level'] = item.difficulty

            item_info['ansName'] = ""
            item_info['readNum'] =''
            item_info['praiseNum'] =''
            item_info['status'] = ''
            item_info['praiseNum'] = ''
            item_info['status'] = ''
            item_info['imgUrl'] = ''
            item_info['language'] = ''
            item_info['languageCode'] = ''

            item_dict['info'] = item_info
            data.append(item_dict)
        json_dict['data'] = data
        return json_dict


def api_all(request):
    post1 = api_mysearch_other(request, 0)
    post2 = api_code_search(request, 0)
    # 每页显示条数
    pageNum = int(request.POST['pageNum'].strip())
    pageSize = int(request.POST['pageSize'].strip())
    title = request.POST['title'].strip()
    query = title.split(' ')
    level = int(request.POST['level'].strip())
    labelType = int(request.POST['labelType'].strip())

    json_dict = {}
    json_dict['code'] = 0
    json_dict['msg'] = "操作成功"
    page_info = {}
    page_info['pageNums'] = pageNum
    page_info['pageSize'] = pageSize
    total_page = math.ceil((len(post1) + len(post2)) / pageSize)
    page_info['pageTotal'] = total_page
    page_info['pageCount'] = len(post1) + len(post2)
    json_dict['pageInfo'] = page_info

    problem_Nums = math.ceil(len(post1) / pageSize)

    data = []
    if pageNum < problem_Nums :       # 只需要 result1
        post1 = post1[(pageNum-1)*pageSize:pageNum*pageSize]
        for item in post1:
            item_dict = {}
            item_dict['id'] = item.id
            item_dict['contentType'] = 2
            item_info = {}
            labels = []
            for la in item.label:
                labels.append(la)
            item_labels = ','.join(labels)
            item_title = item.title
            item_description = item.description
            for Q in query:
                if item_title.lower().find(Q.lower()) > -1:
                    # print(1)
                    pos = re.finditer(Q.lower(), item_title.lower())
                    for pp in pos:
                        # print(item.id,pp.start())
                        length = len(Q)
                        # print(length)
                        res = item_title[pp.start():pp.start() + length]
                    Q_r = '<font>' + res + '</font>'
                    item_title = item_title.replace(res, Q_r)
                else:
                    # print('0000')
                    res = Q
                    Q_r = '<font>' + res + '</font>'
                    item_title = item_title.replace(res, Q_r)
                if item_description.lower().find(Q.lower()) > -1:
                    # print(1)
                    pos = re.finditer(Q.lower(), item_description.lower())
                    for pp in pos:
                        # print(item.id,pp.start())
                        length = len(Q)
                        # print(length)
                        res = item_description[pp.start():pp.start() + length]
                    Q_r = '<font>' + res + '</font>'
                    item_description = item_description.replace(res, Q_r)
                else:
                    # print('0000')
                    res = Q
                    Q_r = '<font>' + res + '</font>'
                    item_description = item_description.replace(res, Q_r)
                if item_labels.lower().find(Q.lower()) > -1:
                    # print(1)
                    pos = re.finditer(Q.lower(), item_labels.lower())
                    for pp in pos:
                        # print(item.id,pp.start())
                        length = len(Q)
                        # print(length)
                        res = item_labels[pp.start():pp.start() + length]
                    Q_r = '<font>' + res + '</font>'
                    item_labels = item_labels.replace(res, Q_r)
                else:
                    # print('0000')
                    res = Q
                    Q_r = '<font>' + res + '</font>'
                    item_labels = item_labels.replace(res, Q_r)
            item_info['title'] = item_title
            item_info['content'] = item_description
            item_info['labels'] = item_labels
            item_info['sourceName'] = item.source
            item_info['createTime'] = item.create_time
            item_info['level'] = item.difficulty
            item_info['ansName'] = ""
            item_info['readNum'] = ''
            item_info['praiseNum'] = ''
            item_info['status'] = ''
            item_info['praiseNum'] = ''
            item_info['status'] = ''
            item_info['imgUrl'] = ''
            item_info['language'] = ''
            item_info['languageCode'] = ''
            item_dict['info'] = item_info
            data.append(item_dict)
    elif pageNum == problem_Nums:
        post1 = post1[(pageNum - 1) * pageSize : ]
        length1 = len(post1)
        if length1==pageSize:
            for item in post1:
                item_dict = {}
                item_dict['id'] = item.id
                item_dict['contentType'] = 2
                item_info = {}
                labels = []
                for la in item.label:
                    labels.append(la)
                item_labels = ','.join(labels)
                item_title = item.title
                item_description = item.description
                for Q in query:
                    if item_title.lower().find(Q.lower()) > -1:
                        # print(1)
                        pos = re.finditer(Q.lower(), item_title.lower())
                        for pp in pos:
                            # print(item.id,pp.start())
                            length = len(Q)
                            # print(length)
                            res = item_title[pp.start():pp.start() + length]
                        Q_r = '<font>' + res + '</font>'
                        item_title = item_title.replace(res, Q_r)
                    else:
                        # print('0000')
                        res = Q
                        Q_r = '<font>' + res + '</font>'
                        item_title = item_title.replace(res, Q_r)
                    if item_description.lower().find(Q.lower()) > -1:
                        # print(1)
                        pos = re.finditer(Q.lower(), item_description.lower())
                        for pp in pos:
                            # print(item.id,pp.start())
                            length = len(Q)
                            # print(length)
                            res = item_description[pp.start():pp.start() + length]
                        Q_r = '<font>' + res + '</font>'
                        item_description = item_description.replace(res, Q_r)
                    else:
                        # print('0000')
                        res = Q
                        Q_r = '<font>' + res + '</font>'
                        item_description = item_description.replace(res, Q_r)
                    if item_labels.lower().find(Q.lower()) > -1:
                        # print(1)
                        pos = re.finditer(Q.lower(), item_labels.lower())
                        for pp in pos:
                            # print(item.id,pp.start())
                            length = len(Q)
                            # print(length)
                            res = item_labels[pp.start():pp.start() + length]
                        Q_r = '<font>' + res + '</font>'
                        item_labels = item_labels.replace(res, Q_r)
                    else:
                        # print('0000')
                        res = Q
                        Q_r = '<font>' + res + '</font>'
                        item_labels = item_labels.replace(res, Q_r)
                item_info['title'] = item_title
                item_info['content'] = item_description
                item_info['labels'] = item_labels
                item_info['sourceName'] = item.source
                item_info['createTime'] = item.create_time
                item_info['level'] = item.difficulty
                item_info['ansName'] = ""
                item_info['readNum'] = ''
                item_info['praiseNum'] = ''
                item_info['status'] = ''
                item_info['praiseNum'] = ''
                item_info['status'] = ''
                item_info['imgUrl'] = ''
                item_info['language'] = ''
                item_info['languageCode'] = ''
                item_dict['info'] = item_info
                data.append(item_dict)
        else:
            for item in post1:
                item_dict = {}
                item_dict['id'] = item.id
                item_dict['contentType'] = 2
                item_info = {}
                labels = []
                for la in item.label:
                    labels.append(la)
                item_labels = ','.join(labels)
                item_title = item.title
                item_description = item.description
                for Q in query:
                    if item_title.lower().find(Q.lower()) > -1:
                        # print(1)
                        pos = re.finditer(Q.lower(), item_title.lower())
                        for pp in pos:
                            # print(item.id,pp.start())
                            length = len(Q)
                            # print(length)
                            res = item_title[pp.start():pp.start() + length]
                        Q_r = '<font>' + res + '</font>'
                        item_title = item_title.replace(res, Q_r)
                    else:
                        # print('0000')
                        res = Q
                        Q_r = '<font>' + res + '</font>'
                        item_title = item_title.replace(res, Q_r)
                    if item_description.lower().find(Q.lower()) > -1:
                        # print(1)
                        pos = re.finditer(Q.lower(), item_description.lower())
                        for pp in pos:
                            # print(item.id,pp.start())
                            length = len(Q)
                            # print(length)
                            res = item_description[pp.start():pp.start() + length]
                        Q_r = '<font>' + res + '</font>'
                        item_description = item_description.replace(res, Q_r)
                    else:
                        # print('0000')
                        res = Q
                        Q_r = '<font>' + res + '</font>'
                        item_description = item_description.replace(res, Q_r)
                    if item_labels.lower().find(Q.lower()) > -1:
                        # print(1)
                        pos = re.finditer(Q.lower(), item_labels.lower())
                        for pp in pos:
                            # print(item.id,pp.start())
                            length = len(Q)
                            # print(length)
                            res = item_labels[pp.start():pp.start() + length]
                        Q_r = '<font>' + res + '</font>'
                        item_labels = item_labels.replace(res, Q_r)
                    else:
                        # print('0000')
                        res = Q
                        Q_r = '<font>' + res + '</font>'
                        item_labels = item_labels.replace(res, Q_r)
                item_info['title'] = item_title
                item_info['content'] = item_description
                item_info['labels'] = item_labels
                item_info['sourceName'] = item.source
                item_info['createTime'] = item.create_time
                item_info['level'] = item.difficulty
                item_info['ansName'] = ""
                item_info['readNum'] = ''
                item_info['praiseNum'] = ''
                item_info['status'] = ''
                item_info['praiseNum'] = ''
                item_info['status'] = ''
                item_info['imgUrl'] = ''
                item_info['language'] = ''
                item_info['languageCode'] = ''
                item_dict['info'] = item_info
                data.append(item_dict)

            query_token = highlight_words(' '.join(query))
            highlight_dict = {}
            for word in query_token.split(" "):
                if word not in highlight_dict:
                    highlight_dict[word] = "<font>" + word + "</font>"
            post2 = post2[ : (pageSize-length1)]
            for item in post2:
                item_dict = {}
                item_dict['id'] = item[1].id
                item_dict['contentType'] = 3
                # 将代码中需要高亮的部分用<font></font>标签标注起来
                for word, replace_word in highlight_dict.items():
                    item[0].code = item[0].code.replace(word, replace_word)
                item_info = {}
                item_info['title'] = item[1].title
                item_info['sourceName'] = item[1].source
                item_info['createTime'] = str(item[1].create_time)
                item_info['level'] = item[1].difficulty
                item_info['labels'] = ""
                item_info['ansName'] = ""
                item_info['content'] = item[0].code
                item_info['readNum'] = ""
                item_info['praiseNum'] = ""
                item_info['status'] = ""
                item_info['imgUrl'] = ""
                item_info['answersNums'] = ""
                item_info['language'] = ""
                item_info['languageCode'] = ""

                item_dict['info'] = item_info
                data.append(item_dict)
    else:  # 全是 result2

        query_token = highlight_words(" ".join(query))
        highlight_dict = {}
        for word in query_token.split(" "):
            if word not in highlight_dict:
                highlight_dict[word] = "<font>" + word + "</font>"
        length2 = pageSize - len(post1) % pageSize  # 交界处的 result2
        if pageNum == total_page:
            post2 = post2[length2+(pageNum-problem_Nums-1)*pageSize:]
        else:
            post2 = post2[length2+pageSize*(pageNum-problem_Nums-1) : length2+pageSize*(pageNum-problem_Nums)]

        for item in post2:
            item_dict = {}
            item_dict['id'] = item[1].id
            item_dict['contentType'] = 2
            # 将代码中需要高亮的部分用<font></font>标签标注起来
            for word, replace_word in highlight_dict.items():
                item[0].code = item[0].code.replace(word, replace_word)
            item_info = {}
            item_info['title'] = item[1].title
            item_info['sourceName'] = item[1].source
            item_info['createTime'] = str(item[1].create_time)
            item_info['level'] = item[1].difficulty
            item_info['labels'] = ""
            item_info['ansName'] = ""
            item_info['content'] = item[0].code
            item_info['readNum'] = ""
            item_info['praiseNum'] = ""
            item_info['status'] = ""
            item_info['imgUrl'] = ""
            item_info['answersNums'] = ""
            item_info['language'] = ""
            item_info['languageCode'] = ""

            item_dict['info'] = item_info
            data.append(item_dict)

    json_dict['data'] = data

    return json_dict

def api_question_result(request):
    pageNum = request.GET['pageNum'].strip()  # 页码
    pageSize = request.GET['pageSize'].strip()  # 每页条数

    query = request.GET['title'].strip()
    if query == '':
        posts = SearchQuerySet().using('question').models(Question).all()
    else:
        posts = SearchQuerySet().using('question').models(Question).filter(content = query)

    result_num = posts.count()

    if True:
        json_dict = {}
        json_dict['code'] = 0
        json_dict['msg'] = "操作成功"
        page_info = {}
        page_info['pageNums'] = pageNum
        page_info['pageSize'] = pageSize
        total_page = math.ceil(result_num / pageSize)  # 浮点数向上取整
        page_info['pageTotal'] = total_page
        page_info['pageCount'] = 0
        json_dict['pageInfo'] = page_info
        if request.GET['pageNums'] == total_page:
            returned_posts = posts[(pageNum - 1) * pageSize:]
        else:
            returned_posts = posts[
                             (pageNum - 1) * pageSize: pageNum * pageSize]
        data = []
        for item in returned_posts:
            item_dict = {}
            item_dict['id'] = item.id
            item_dict['contentType'] = 1

            item_info = {}
            item_info['title'] = item.title
            item_info['sourceName'] = ''
            item_info['createTime'] = ''
            item_info['level'] = ''
            item_info['labels'] = ''

            item_info['ansName'] = ''
            item_info['answer'] = ''
            item_info['answerNums'] = ''

            item_info['content'] = item.question_text
            item_info['readNum'] = ''
            item_info['praiseNum'] = ''
            item_info['status'] = ''
            item_info['imgUrl'] = ''
            item_info['language'] = ''
            item_info['languageCode'] = ''

            item_dict['info'] = item_info
            data.append(item_dict)
        json_dict['data'] = data
        return json_dict

def api_detail_question(request):

    id = int(request.GET['id'].strip())
    post = Question.objects.filter(id = id)
    json_dict = {}

    json_dict['code'] = 0
    json_dict['msg'] = "操作成功"

    data = {}
    data['id'] = id
    data['title'] = post.question_text
    data['labels'] = ''
    data['leave'] = ''
    data['brief'] = post.answer_text

    data['content'] = ''
    data['answerResult'] = ''
    data['createTime'] = ''
    data['userName'] = ''
    data['userId'] = ''
    data['readNum'] = ''
    data['praiseNum'] = ''
    data['thinking'] = ''
    data['arithmetric'] = ''
    data['languageCode'] = ''

    json_dict['data'] = data

    return json_dict

def api_detail_problemcode(request):
    id = request.GET['id'].strip()
    problem_obj = Problem.objects.filter(id = id)
    problemcode_obj = ProblemCode.objects.filter(problem_id_id = id)
    json_dict = {}

    json_dict['code'] = 0
    json_dict['msg'] = "操作成功"

    data = {}
    data['id'] = id
    data['title'] = problem_obj.title
    data['labels'] = ""
    data['leave'] = problem_obj.difficulty
    data['brief'] = ""
    data['content'] = problemcode_obj.code
    data['answerResult'] = ""
    data['createTime'] = None
    data['userName'] = ""
    data['userId'] = ""
    data['readNum'] = 0
    data['praiseNum'] = 0
    data['thinking'] = ""
    data['arithmetric'] = ""
    data['languageCode'] = None

    json_dict['data'] = data

    return json_dict

def api_search_result(request):

    if int(request.POST['menuType']) == 2:
        json_dict = api_code_search(request)

    elif int(request.POST['menuType']) == 1:
        json_dict = api_mysearch_other(request)

    elif int(request.POST['menuType']) == 0:
        json_dict = api_all(request)

    elif int(request.POST['menuType']) == 3:
        json_dict = api_question_result(request)

    return HttpResponse(json.dumps(json_dict, ensure_ascii=False))

def api_detail(request):     # 搜索详情信息

        if int(request.GET['contentType'])==3:
            json_dict = api_detail_question(request)

        elif int(request.GET['contentType']) == 2:
            json_dict = ""

        elif int(request.GET['contentType']) == 1:
            json_dict = ""

        return HttpResponse(json.dumps(json_dict, ensure_ascii=False))

#