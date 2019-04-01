from django.shortcuts import render, redirect
from .forms import UserForm, RegisterForm
from .models import User
from .utils import hash_code
from django.http import HttpResponse


# Create your views here.

def index(request):
    return render(request, "account/index.html")

def login(request):
    # 不允许重复登录
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session.set_expiry(0)
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'account/login.html', locals())

    login_form = UserForm()
    return render(request, "account/login.html", locals())

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册
        return redirect('/index/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            education_level = register_form.cleaned_data['education_level']
            learning_language = ','.join(register_form.cleaned_data['learning_language'])
            program_time = register_form.cleaned_data['program_time']
            birth = register_form.cleaned_data['birth']
            for character in username:
                if u'\u4e00' <= character <= u'\u9fff':
                    message = "请输入英文字符或数字！"
                    return render(request, 'account/register.html', locals())
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'account/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在，请重新选择用户名！'
                    return render(request, 'account/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册， 请使用别的邮箱！'
                    return render(request, 'account/register.html', locals())
                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.education_level = education_level
                new_user.learning_language = learning_language
                new_user.program_time = program_time
                new_user.birth = birth
                new_user.save()
                return redirect('/login/') #  自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'account/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')
