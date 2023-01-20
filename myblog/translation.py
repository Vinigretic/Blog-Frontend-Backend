from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('h1', 'title', 'description', 'content')


