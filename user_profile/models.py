from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to='uploads/profilePic', blank=True, null=True)

    def __str__(self):
        return f'{self.user.id}--{self.user}'


# class UserMessage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.CharField(max_length=255, blank = True, null = True)

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_media = models.FileField(upload_to='uploads/userMedia', blank = True, null = True)
    post_description = models.CharField(max_length=255, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.id}--{self.user}'


