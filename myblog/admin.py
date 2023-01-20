from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

