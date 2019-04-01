import datetime

from django import forms
import hashlib


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    e_level = (
        ('1', '大学'),
        ('2', '高中'),
        ('3', '初中'),
        ('4', '小学'),
    )
    l_language = (
        ('1', 'python'),
        ('2', 'c++'),
        ('3', 'c语言'),
        ('4', 'java'),
    )
    p_time = (
        ('1', '初学'),
        ('2', '1年'),
        ('3', '2年'),
        ('4', '2年以上'),
    )

    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 40, cur_year)][::-1])

    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    education_level = forms.ChoiceField(label='教育程度', choices=e_level)
    learning_language = forms.MultipleChoiceField(label='学习语言',
                                                  choices=l_language,
                                                  error_messages={'required': '请选择您要学习的语言'},
                                                  widget=forms.CheckboxSelectMultiple()
                                                  )
    program_time = forms.ChoiceField(label='编程时间', choices=p_time)
    birth = forms.DateField(initial=datetime.date.today(),
                            widget=forms.SelectDateWidget(years=year_range), label="出生年月")