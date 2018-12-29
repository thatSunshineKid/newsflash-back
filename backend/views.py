# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from.serializers import PostSerializer
from rest_framework import generics
from .models import Author, Post

# Create your views here.


class NewsbotList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer