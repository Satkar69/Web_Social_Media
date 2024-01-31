from django.contrib import admin
from .models import Post, PostComment, PostApply, PostReaction, UserConversation
# Register your models here.


admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostApply)
admin.site.register(PostReaction)
admin.site.register(UserConversation)