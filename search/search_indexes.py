# -*-coding:utf-8 -*-
__author__ = '$'

import codecs
from haystack import indexes
from django.shortcuts import loader
from .models import Problem, ProblemCode,Question
from .code_processing.ast_cpp import convert_cpp
from .code_processing.ast_python import convert_python
from .code_processing.code_utility import cpp_head_remove
from .code_processing.tokenize import tokenize


# -----要相对某个app进行索引，就在那个其文件夹下建search_index.py
#
class ProblemIndex(indexes.SearchIndex, indexes.Indexable):

   text = indexes.CharField(document=True,use_template=True)   #该字段是主要进行关键字查询的字段,该字段的索引值可以由多个数据库模型类字段组成，具体由哪些模型类字段组成，我们用use_template=True表示后续通过模板来指明

   id = indexes.IntegerField(model_attr='id')
   title = indexes.CharField( model_attr='title')
   describe = indexes.CharField(model_attr='description')
   difficult = indexes.IntegerField(model_attr='difficulty')

   label = indexes.MultiValueField()

   def get_model(self):           #重载get_model方法，必须要有！
       return Problem

   def index_queryset(self, using=None):
       return self.get_model().objects.all()    #确定在建立索引时有些记录被索引，这里我们简单地返回所有记录

   def prepare_label(self,obj):
       return [ la.label_name for la in obj.label.all()]


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    # question_text = indexes.CharField(model_attr='question_text')
    # anwser_text = indexes.CharField(model_attr='answer_text')

    def get_model(self):           #重载get_model方法，必须要有！

       return Question

    def index_queryset(self, using=None):
       return self.get_model().objects.all()    #确定在建立索引时有些记录被索引，这里我们简单地返回所有记录


class ProblemCodeIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    id = indexes.CharField(model_attr='id')
    code = indexes.CharField(model_attr='code')
    problem = indexes.IntegerField(model_attr='problem_id_id')
    language = indexes.IntegerField(model_attr='language_id_id')

    def get_model(self):
        return ProblemCode

    def index_queryset(self, using=None):     # 返回要建立索引的数据查询集
       return self.get_model().objects.all()

    def prepare(self, obj):
        data = super(ProblemCodeIndex, self).prepare(obj)
        code_text = obj.code

        code_str = tokenize(code_text, "char") + " " + tokenize(code_text, "lex")
        # print(code_str)

        if obj.language_id_id == 2 or obj.language_id_id == 3:    # 如果是处理python代码
            # code_text = codecs.decode(code_text, 'unicode_escape')
            try:
                python_str = convert_python(code_text)
                code_str += python_str
            except:
                python_str = "null"
                code_str += ""
            # print('ID:', obj.id, ' Python: ', python_str)

            # t = loader.select_template(('search/indexes/search/problemcode_text.txt',))
            # data['text'] = t.render({'object': obj, 'code_string': code_str})

        elif obj.language_id_id == 1:  # 如果是处理C++代码
            # code_text = codecs.decode(code_text, 'unicode_escape')
            code_text = cpp_head_remove(code_text)
            try:
                cpp_str = convert_cpp(code_text)
                code_str += cpp_str
            except:
                cpp_str = "null"
                code_str += ""
            # print('ID:', obj.id, ' C++: ', cpp_str)

            # t = loader.select_template(('search/indexes/search/problemcode_text.txt',))
            # data['text'] = t.render({'object': obj, 'code_string': code_str})
        # except:
        print('ID:', obj.id, ' ', code_str)

        t = loader.select_template(('search/indexes/search/problemcode_text.txt',))
        data['text'] = t.render({'object': obj, 'code_string': code_str})
        return data

    def prepare_id(self, obj):
        return obj.id

    def prepare_code(self, obj):
        return obj.code

    def prepare_problem(self, obj):
        return obj.problem_id_id

    def prepare_language(self, obj):
        return obj.language_id_id








