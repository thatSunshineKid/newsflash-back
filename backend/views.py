# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from.serializers import PostSerializer, CreateAuthorSerializer, UserSerializer, LoginUserSerializer, CreatePostSerializer
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

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)
        })

class CreatePostAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CreatePostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response({
            "post": PostSerializer(post, context=self.get_serializer_context()).data
            })

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PostSerializer

    def get_queryset(self):
        current_user = self.request.user.author
        return Post.objects.filter(author_id=current_user.id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

