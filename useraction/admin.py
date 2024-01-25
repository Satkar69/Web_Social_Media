from django.contrib import admin
from .models import Post, PostComment, PostBid, PostReaction
# Register your models here.


admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostBid)
admin.site.register(PostReaction)