from django.db import models
from userprofile.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Post(models.Model):
    added_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=False)
    media = models.FileField(upload_to='uploads/mediapost', blank=True, null=True)
    
    def __str__(self) -> str:
        return self.added_by.username + ' / ' + f'{self.id}' + ' / ' + self.description


class PostComment(models.Model):
    commented_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=True, null=False)

    def __str__(self) -> str:
        return self.commented_by.username


class PostApply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    applied_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.applied_by.username + ' / ' + f'{self.id}' + ' / ' + f'{self.post}'


class PostReaction(models.Model):
    reacted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default = False)

    def __str__(self) -> str:
        return 'reacted_by -' + ' ' + self.reacted_by.username + ' / ' + self.post.added_by.username + ' / ' + f'{self.post.id}' + ' / ' + self.post.description


class UserConversation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    applicant = models.ForeignKey(PostApply, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.message_by.username + ' / ' + f'{self.id}' + ' / ' + f'post - {self.post.description}'
        
