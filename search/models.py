from django.db import models

# Create your models here.
class Problem(models.Model):
    '''问题表'''
    title = models.TextField(blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    input_sample = models.TextField(blank=True, null=True)  # 用户输入样例
    output_sample = models.TextField(blank=True, null=True) # 用户输出样例
    testcase_folder = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    source = models.TextField(blank=True, null=True)
    time_limit = models.IntegerField(default=3000)  # 单位为ms
    memory_limit = models.IntegerField(default=65536)   # 单位为KB

    # label = models.ManyToManyField('Label', verbose_name='标签', blank=True,null=True)
    label = models.ManyToManyField('Label', verbose_name='标签', blank=True)

    spare = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'problem'

class Language(models.Model):
    '''语言表'''
    language = models.CharField(max_length=20)

    class Meta:
        db_table = 'language'

class ProblemCode(models.Model):
    '''问题代码表'''
    problem_id = models.ForeignKey('Problem', on_delete=models.CASCADE)
    language_id = models.ForeignKey('Language', on_delete=models.CASCADE)
    code = models.TextField()

    class Meta:
        db_table = 'problemCode'

class Label(models.Model):
    '''标签表'''
    label_name = models.CharField(max_length=20)
    father_id = models.ForeignKey('self', verbose_name='父节点', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'label'

class Question(models.Model):
    '''问答表'''
    question_text = models.TextField()
    question_code = models.TextField(blank=True, null=True)
    answer_text = models.TextField(blank=True, null=True)
    answer_code = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=256, blank=True, null=True)
    spare = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'question'