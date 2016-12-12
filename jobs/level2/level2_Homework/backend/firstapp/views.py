from django.shortcuts import render, redirect

from firstapp.models import Article, Comment, Ticket, Profile
from firstapp.forms import CommentForm, ProfileForm

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Create your views here.

def myinfo(request):
    # 必须先登录，否则跳转至首页
    if not isinstance(request.user, User):
        return redirect(to="index")

    context = {}

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # 1.修改名字
            Realname = form.cleaned_data["Realname"]
            password = form.cleaned_data["password"]
            # 获取用户的User对象
            user_object = User.objects.get(username=request.user)
            # 把验证后的名字赋值给用户对象的username变量
            if Realname:
                user_object.username = Realname
            # 2.修改密码
            if password:
                user_object.set_password(password)
            # 一定要保存User对象才能生效
            user_object.save()
            # c = Profile(belong_to=user_object)
            # c.save()

            #+++++++++++++++++++++++++++++++++++++++++++++++++++
            # 下面是保存数据到Profile表中，反向查询
            # 3.修改性别
            sex = form.cleaned_data["sex"]
            if sex:
                user_object.profile.sex = sex

            # 4.修改/上传头像
            avatar = form.cleaned_data["avatar"]
            if avatar:
                user_object.profile.avatar = avatar

            user_object.profile.save()

            # 5.提交修改后，自动以新的用户名和密码登录
            newuser = authenticate(username=user_object.username, password=password)
            login(request, newuser)

            return redirect(to="myinfo")

    if request.method == "GET":
        form = ProfileForm()
    context = {'form': form}
    return render(request, "myinfo.html", context)


def mycollection(request):
    if not isinstance(request.user, User):
        return redirect(to="index")

    # 筛选出当前user选择了like的Ticket对象列表
    user = request.user
    user_collect_article_list = Ticket.objects.filter(voter=user, choice="like")
    # for i in user_collect_article_list:
    #     print("+++++++++++")
    #     print(i.voter)
    #     print(i.article.id, i.article.img)

    context = {}

    page_robot = Paginator(user_collect_article_list, 3)
    page_num = request.GET.get('page')
    try:
        user_collect_article_list = page_robot.page(page_num)
    except EmptyPage:
        user_collect_article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        user_collect_article_list = page_robot.page(1)
    context = {'user_collect_article_list': user_collect_article_list}

    return render(request, 'mycollection.html', context)


def index(request):
    article_list = Article.objects.all()

    page_robot = Paginator(article_list, 9)
    page_num = request.GET.get('page')
    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        article_list = page_robot.page(1)

    context = {}
    context["article_list"] = article_list

    return render(request, 'index.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)

    if request.method == "GET":
        form = CommentForm

    context = {}
    context["article"] = article
    context['form'] = form

    return render(request, 'detail.html', context)

def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]
            article = Article.objects.get(id=id)
            c = Comment(name=name, comment=comment, belong_to=article)
            c.save()
            return redirect(to="detail", id=id)
    return redirect(to="detail", id=id)

def index_login(request):
    if request.method == "GET":
        form = AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to="index")

    context = {}
    context['form'] = form

    return render(request, 'login.html', context)

def index_register(request):
    if request.method == "GET":
        form = UserCreationForm

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # ############################
            # print(request.POST.get("username"))
            # print(request.user)
            # 注册后为用户创建Profile，设置一对一关系
            user_object = User.objects.get(username=request.POST.get("username"))
            c = Profile(belong_to=user_object)
            c.save()
            ############################
            return redirect(to='login')

    context = {}
    context['form'] = form

    return render(request, 'register.html', context)

def vote(request, id):
    # 未登录用户不允许投票，自动跳回详情页
    if not isinstance(request.user, User):
        return redirect(to="detail", id=id)

    voter_id = request.user.id

    try:
        # 如果找不到登陆用户对此篇文章的操作，就报错
        user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=id)
        user_ticket_for_this_article.choice = request.POST["vote"]
        user_ticket_for_this_article.save()

    except ObjectDoesNotExist:
        new_ticket = Ticket(voter_id=voter_id, article_id=id, choice=request.POST["vote"])
        new_ticket.save()

    # 如果是点赞，更新点赞总数
    if request.POST["vote"] == "like":
        article = Article.objects.get(id=id)
        article.likes += 1
        article.save()

    return redirect(to="detail", id=id)
