from django.contrib import admin
from workapp.models import *

# Register your models here.

admin.site.register(Area)
admin.site.register(HouseInfo)
admin.site.register(UserInfo)
admin.site.register(Collect)

# 超级管理员账号密码: Admin/Admin123456
