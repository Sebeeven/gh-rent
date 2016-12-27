from django.shortcuts import render, redirect
from website.form import LoginForm
from django.contrib.auth import authenticate, login

def video_list(request):
    return render(request, 'mobile_list.html', {})

# 页面1：/m/userlistpanel/
def userlistpanel(request):
    return render(request, 'userListPanel.html', {})

# 页面2：/m/userlistpanel/login/
def userlogin(request):
    error_msg = ''
    context = {}
    if request.method=='GET':
        form = LoginForm
    elif request.method=='POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_superuser:
                    login(request, user)
                    print('superuser login success!')
                    return redirect(to='userlistpanel')
                else:
                    error_msg = "你没有权限登录！"
            else:
                error_msg = "用户名或密码错误！"

    context = {'form': form, 'error_msg': error_msg}
    return render(request, 'userListPanelLogin.html', context)


# 页面3：/m/userdetail/
def userdetail(request):
    return render(request, 'userDetail.html', {})
