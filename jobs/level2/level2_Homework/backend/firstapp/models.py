from django.db import models

from django.contrib.auth.models import User
from faker import Factory

# Create your models here.
class Profile(models.Model):
    belong_to = models.OneToOneField(to=User,related_name='profile',null=True)
    avatar = models.ImageField(upload_to=".", null=True)
    SEX_CHOICES = (
        ('Gender', '性别'),
        ('Male', '男'),
        ('Female', '女'),
    )
    sex = models.CharField(null=True, blank=True, max_length=20, choices=SEX_CHOICES)

    def __str__(self):
        return str(self.belong_to)

# class User_Collect_Article(models.Model):
#     collector = models.ManyToManyField(to=User, related_name='collector', null=True)
#     collection = models.ManyToManyField(to=Article, related_name='collection', null=True)
#
#     def __str__(self):
#         return str(self.id)

class Article(models.Model):
    title = models.CharField(max_length=500)
    img = models.CharField(null=True, blank=True, max_length=250)
    content = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    createtime = models.DateField()

    def __str__(self):
        return self.title

# # 生成假数据，python3 manage.py runserver后会自动生成,生成完成后请注释。
# f = open('firstapp\image_url.txt', 'r')
# fake = Factory.create()
#
# for url in f.readlines():
#     print(url)
#     article = Article(
#         title = fake.text(max_nb_chars=90),
#         img = url,
#         content = fake.text(max_nb_chars=3000),
#         views = fake.random_digit(),
# 		likes = fake.random_digit(),
# 		createtime = fake.date_time_this_month(),
#     )
#     article.save()



class Comment(models.Model):
    name = models.CharField(max_length=500)
    avatar = models.CharField(max_length=250, default="static/images/default.png")
    comment = models.TextField(null=True, blank=True)
    createtime = models.DateField(auto_now=True)

    belong_to = models.ForeignKey(to=Article, related_name="under_comments", null=True, blank=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    voter = models.ForeignKey(to=User, related_name="user_tickets")
    article = models.ForeignKey(to=Article, related_name="article_tickets")

    ARTICLE_CHOICES = {
        ("like", "like"),
        ("dislike", "dislike"),
        ("normal", "normal")
    }
    choice = models.CharField(choices=ARTICLE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)
