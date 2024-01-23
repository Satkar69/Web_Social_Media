from django.contrib import admin
from .models import UserPost, UserDetail

# Register your models here.

admin.site.register(UserDetail)
admin.site.register(UserPost)