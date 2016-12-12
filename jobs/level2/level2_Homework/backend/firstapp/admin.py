from django.contrib import admin

# Register your models here.
from firstapp.models import Article, Comment, Profile #, Ticket

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Profile)
# admin.site.register(Ticket)
