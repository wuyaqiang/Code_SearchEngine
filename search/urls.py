from django.urls import path
from . import search_views

urlpatterns = [
    path("search1/", search_views.mysearch, name="my_search"),
    path("search1/<int: problem_id>", search_views.problem_detail),
    path("search2/<int: problem_id>", search_views.problem_detail),
    path("search2/", search_views.mysearch_other),
    path("find_answer/", search_views.question_answer),
    path("find_question/", search_views.find_question),
    path("search_question/<int: problem_id>", search_views.question_detail),
    path("search_question/", search_views.question_result, name="question_result"),
    path("search_test/", search_views.problem_search),
    path("search_result/", search_views.result_search),
    path("code_search_result/", search_views.code_search),
]
