from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, User

# Create your models here.
class CustomUserProfile(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        """ Create a new user profile """
        if not username:
            raise ValueError('User must have usernmame')
        user = self.model(first_name = first_name, last_name = last_name, username=username, email = email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """ Create a new superuser profile """
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system """
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField( max_length=255, null=True, blank=True)
    last_name = models.CharField( max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    profile_picture = models.FileField(upload_to='uploads/userprofile', null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    
    objects = CustomUserProfile()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
