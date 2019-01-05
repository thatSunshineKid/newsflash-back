# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from.serializers import PostSerializer, CreateAuthorSerializer, UserSerializer
from rest_framework import generics, viewsets, permissions
from .models import Author, Post

from rest_framework.response import Response
from knox.models import AuthToken


# Create your views here.


class NewsbotList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class TechpostList(generics.ListAPIView):
    queryset = Post.objects.filter(tags__in=[4])
    serializer_class = PostSerializer


class SportspostList(generics.ListAPIView):
    queryset = Post.objects.filter(tags__in=[2])
    serializer_class = PostSerializer

class PoliticspostList(generics.ListAPIView):
    queryset = Post.objects.filter(tags__in=[1])
    serializer_class = PostSerializer


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateAuthorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "author": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })

