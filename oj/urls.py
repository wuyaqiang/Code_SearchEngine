from django.urls import path
from . import views


urlpatterns = [
    # path("", views.question_bank, name="question_bank"),
    # path('<int:question_id>/', views.question_detail, name="question_detail"),
    # path('<int:question_id>/result', views.question_result, name="question_result"),
]

# path("question_bank/", views.question_bank, name="question_bank"),
# path("question_bank/<int: problem_id>", views.problem_detail, name="problem_detail"),
# path("question_bank/<int: problem_id>/result", views.problem_submission, name="problem_submission"),