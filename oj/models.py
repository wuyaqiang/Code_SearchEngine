from django.db import models

# Create your models here.
from django.db import models
from search.models import Problem, Language
from account.models import User

class JudgeStatus:
    COMPILE_ERROR = -2
    WRONG_ANSWER = -1
    ACCEPTED = 0
    CPU_TIME_LIMIT_EXCEEDED = 1
    REAL_TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5
    PENDING = 6
    JUDGING = 7
    PARTIALLY_ACCEPTED = 8

class Submission(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    submit_time = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    result = models.IntegerField(db_index=True, default=JudgeStatus.PENDING)
    spare = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = "submission"

class Special_judge(models.Model):
    spj_code = models.TextField()
    spj_language = models.ForeignKey(Language, on_delete=models.CASCADE)
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)

    class Meta:
        db_table = "spj"