from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from workapp.forms import RegisterForm, LoginForm, AlterUserForm
from workapp.models import UserInfo
# Create your views here.


def index(request):
    context={}
    return render(request, 'index.html', context)

def list(request):
    context={}
    return render(request, 'list.html', context)

def detail(request):
    context={}
    return render(request, 'detail.html', context)

def userinfo(request):
    if not isinstance(request.user, User):
        return redirect(to="index")

    context={}
    # if request.method == 'POST':
    return render(request, 'personcenter.html', context)

def alteruser(request):
    if not isinstance(request.user, User):
        return redirect(to="index")

    context={}
    if request.method == 'POST':
        form = AlterUserForm(request.POST)
        if form.is_valid():
            alterusername = form.cleaned_data["username"]
            alterpassword = form.cleaned_data["password"]
            # alteravatar = form.cleaned_data["avatar"]
            user_object = User.objects.get(username=request.user)
            if alterusername:
                user_object.username = alterusername
            if alterpassword:
                user_object.set_password(alterpassword)
            user_object.save()

            newuser = authenticate(username=user_object.username, password=alterpassword)
            login(request, newuser)
            return redirect(to="alteruser")

    if request.method == 'GET':
        form = AlterUserForm()
    context = {'form': form}
    return render(request, 'personmodify.html', context)

def index_login(request):
    error_msg = ""
    context = {}
    if request.method == "GET":
        form = LoginForm

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user_object = User.objects.get(email=email)
                user = authenticate(username=user_object.username, password=password)
                if not user:
                    error_msg = "邮箱或密码错误"
                else:
                    login(request, user)
                    return redirect(to="index")
            except ObjectDoesNotExist:
                error_msg = "邮箱或密码错误"

    context = {'form': form, 'error_msg': error_msg}
    return render(request, 'login.html', context)

def index_register(request):
    context={}
    if request.method == "GET":
        form = RegisterForm

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            user_object = User.objects.create_user(username, email, password)
            c = UserInfo(name=user_object, password=password, email=email)
            c.save()
            return redirect(to='login')

    context = {'form': form}
    return render(request, 'register.html', context)




def appointment(request):
    context={}
    return render(request, 'appointment.html', context)
