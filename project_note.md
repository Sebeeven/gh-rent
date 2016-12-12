## 一、关于git的操作：
* 拷贝工程文件到本地并进入进入工程目录：   
```bash
git clone https://git.oschina.net/xxx.git 
cd projectwork/ 
```

* 创建django工程和应用app:  
```bash
django-admin startproject mysite  
cd mysite/  
python3 manage.py startapp app1
```

* git提交至远程仓库：
```bash  
git checkout test #进入test分支（通常master分支已作保护，不能修改）
git pull #更新远程文件到本地  
git add projectwork/* #提交到index暂存区中；  
git commit -m '修改信息' #提交至本地仓库中；  
git push #提交至远程仓库中；  
```
完成。

## 二、关于django的一些问题及解决方法：
### ImageField问题  
1、models.py中建立的Article类，用到的ImageField()数据类型，makemigrations时提示先安装Pillow插件，在python3环境下，pip3 install Pillow提示没找到相关源(python2环境下pip install是正常的），需到官网下载对应版本的Pillow(我下载的是mac的cp3.5版本.whl文件)，安装成功后即不报错。

2、ImageField(upload_to="")有upload_to参数指定图片文件上传路径。  

```python
class Article(models.Model):  
    img = models.ImageField(upload_to="upload_imgs/")  
```


3､ 在admin后台是可以添加图片的，但要把图片取出来在html上显示出来，就出现图片路径问题，stackoverflow上的一个解决办法是：

+ settings.py中添加:

```python
MEDIA_ROOT = os.path.join(BASE_DIR,'media')  
MEDIA_URL = '/media/'
```

+ urls.py中添加：

```python
from django.conf import settings
from django.conf.urls.static import static
...
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
```

+ index.html中添加：

```html
{% for article in article_list %}
...  
	<img src="{{ article.img.url }}" alt="" class="img" />
...  
{% endfor %}
```

到此就解决了图片显示路径问题，工程目录下会自动增加media/upload_imgs/文件夹，上传的图片都存放在这里，而在index.html页面上“检查”图片元素时，图片url也应该是这个路径。

## 三、关于python3调用beautifulsoup4库的问题
下载最新beautifulsoup4并解压，在beautifulsoup4文件夹下进行转码后安装:
```bash  
2to3-3.5 -w bs4  
python3 setup.py install  
```
python3下验证是否成功：
```python
import bs4
```
不报错说明成功安装。


## 四、reqwest
- json和ajax  
- reqwest写法：

```javascript
reqwest({  
    url: "",
    type: "json",
    method: "get",
    data: {},
    success: functions(){
        },
})
```

## 五、密码比对
```python
from django.contrib.auth.hashers import make_password, check_password
print("+++++++++++++++")
print("后台用户名")
print(ps.username)
print("后台密码")
print(ps.password)
print("+++++++++++++++")
#######
hash_password = make_password(data_password,None,'pbkdf2_sha256')
print("登录时提交的密码")
print(data_password)
print("登录时提交的密码hash后")
print(hash_password)
print("+++++++++++++++")
ps_bool = check_password(data_password, ps.password)
print("两密码对比")
print(ps_bool)
print("+++++++++++++++")
is_exist = User.objects.filter(email=data_email, password=data_password).exists()
print("是否能找到用户is_exist")
print(is_exist)
```