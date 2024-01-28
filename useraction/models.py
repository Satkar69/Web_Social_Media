from django.db import models
from userprofile.models import UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Post(models.Model):
    added_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=False)
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


class PostBid(models.Model):
    bid_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.bid_by.username


class PostReaction(models.Model):
    reacted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default = False)

    def __str__(self) -> str:
        return 'reacted_by -' + ' ' + self.reacted_by.username + ' / ' + self.post.added_by.username + ' / ' + f'{self.post.id}' + ' / ' + self.post.description
