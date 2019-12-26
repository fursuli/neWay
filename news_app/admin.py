from django.contrib import admin
from .models import Newsmaker, Post, PostAdmin, Comment, CommentAdmin

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.register(Newsmaker)
