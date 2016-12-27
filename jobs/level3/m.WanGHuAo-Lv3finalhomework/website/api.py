from website.models import Video, UserProfile
from website.form import CreateForm, ModifyForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication


## 功能：用户信息表的序列化
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('id', 'username', 'email', 'profile')
        depth = 1

## 功能：获取一个用户的信息
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def person(request,id):
    try:
        user = User.objects.get(id=id)
        serializer = UserListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'msg':'cannot get this person\'s info'}, status=status.HTTP_403_FORBIDDEN)

## 功能：修改用户信息
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def modifyinfo(request,id):
    try:
        user_object = User.objects.get(id=id)
        form = ModifyForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if User.objects.filter(username=username).count() is not 0:##判断输入的用户名是否与其它用户的名字重复
                if user_object.username != username:##输入的用户名是重复的，判断是与其他的用户名重复还是与自己本来的用户名相同
                    return Response({'msg':'username is exist, please re-enter!'}, status=status.HTTP_403_FORBIDDEN)
            user_object.username = username
            user_object.set_password(password)
            user_object.save()
            return Response({'msg':'modify successfully!'}, status=status.HTTP_200_OK)
        return Response({'msg':'invalid error!'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'msg':'cannot modify!'}, status=status.HTTP_403_FORBIDDEN)

## 功能：非超级用户列表接口
@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
def userlist_api(request):
    user_list = User.objects.filter(is_superuser=False)
    if request.method == 'GET':
        serializer = UserListSerializer(user_list, many=True)
        return Response(serializer.data)

## 功能：删除用户
@api_view(['DELETE'])
@authentication_classes((TokenAuthentication,))
def deleteuser(request,id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response({'msg':'delete is done!'},status=status.HTTP_200_OK)
    except:
        return Response({'msg':'cannot delete!'},status=status.HTTP_403_FORBIDDEN)

## 功能：禁止用户
@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
def banuser(request,id):
    try:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return Response({'msg':'ban is done!'},status=status.HTTP_200_OK)
    except:
        return Response({'msg':'cannot ban!'},status=status.HTTP_403_FORBIDDEN)

## 功能：邀请用户
@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
def inviteuser(request,id):
    try:
        user = User.objects.get(id=id)
        user.profile.vocation = 'author'
        user.save()
        user.profile.save()
        return Response({'msg':'invite is done!'},status=status.HTTP_200_OK)
    except:
        return Response({'msg':'cannot invite!'},status=status.HTTP_403_FORBIDDEN)


## 功能：创建用户
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def createuser(request):
    form = CreateForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        vocation = form.cleaned_data['vocation']
        print("the form is valid!")
        # print(username,password,email,vocation)
        if User.objects.filter(username=username).count() is not 0:
            return Response({'msg':'username is already exist!'}, status=status.HTTP_403_FORBIDDEN)
        if User.objects.filter(email=email).count() is not 0:
            return Response({'msg':'email is already exist!'}, status=status.HTTP_403_FORBIDDEN)

        adduser = User.objects.create_user(username=username, email=email, password=password)
        profile = UserProfile(vocation=vocation, belong_to=adduser)
        profile.save()
        return Response({'msg':'create user successfully!'}, status=status.HTTP_201_CREATED)
    return Response({'msg':'invalid error!'}, status=status.HTTP_400_BAD_REQUEST)


#######################################################

class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=1)
    class Meta:
        model = Video
        fields = '__all__'
        depth = 1

@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def video(request):
    # print(request.user)
    # print(request.auth)
    video_list = Video.objects.order_by('-id')
    if request.method == 'GET':
        if request.auth:
            serializer = VideoSerializer(video_list, many=True)
            return Response(serializer.data)
        else:
            serializer = VideoSerializer(video_list[:5], many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        body = {
            'body': serializer.errors,
            'msg': '40001'
        }
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
def video_card(request, id):
    video_card = Video.objects.get(id=id)
    if request.method == 'PUT':
        serializer = VideoSerializer(video_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if request.user.profile == video_card.owner:
            video_card.delete()
            return Response({'msg': 'A-OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'You can\'t touch this'}, status=status.HTTP_403_FORBIDDEN)
