from django.forms import ModelForm
from useraction.models import *


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields ='__all__'
