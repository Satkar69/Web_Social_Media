from django.db import models
from userprofile.models import UserProfile
# Create your models here.


class UserPost(models.Model):
    added_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=False)
    description = models.CharField(max_length=255, blank=True, null=False)
    media = models.FileField(upload_to='uploads/mediapost')
    