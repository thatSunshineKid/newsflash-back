# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Author, Source, Post, Tag, Subtag, Comment, Like

# Register your models here.

admin.site.register(Author)
admin.site.register(Source)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Subtag)
admin.site.register(Comment)
admin.site.register(Like)

