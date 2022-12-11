from django.contrib import admin
from .models import Post, User
# Register your models here.

@admin.register
class PostModelAdmin(admin.ModelAdmin):#to give action
     list_display = ['id','title','desc']

admin.site.register(Post)
admin.site.register(User)
