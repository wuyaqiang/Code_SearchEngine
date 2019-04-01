# Create your models here.
from django.db import models

# coding: utf8
# Create your models here.
class User(models.Model):
    '''用户表'''

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32)
    register_time = models.DateTimeField(auto_now_add=True)
    birth = models.DateField(blank=True, null=True)
    education_level = models.IntegerField(default=1)
    learning_language = models.CharField(max_length=30)
    program_time = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user"