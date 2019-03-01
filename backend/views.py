# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from.serializers import *
from rest_framework import generics, viewsets, permissions
from .models import *
from .permissions import IsAuthorOrReadOnly

from rest_framework.response import Response
from knox.models import AuthToken


# Create your views here.


# --------- NEW STUFF BELOW -------------------


class PostListView(generics.ListCreateAPIView):
    permission_classes = [ permissions.IsAuthenticated, ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ permissions.IsAuthenticated, IsAuthorOrReadOnly,]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = SimpleTagSerializer

class TagView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SimpleTagSerializer
    queryset = Tag.objects.all()

class SubtagListView(generics.ListCreateAPIView):
    queryset = Subtag.objects.all()
    serializer_class = SimpleSubtagSerializer

class SubtagView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SimpleSubtagSerializer
    queryset = Subtag.objects.all()

# --------- NEW STUFF ABOVE -------------------


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

class UpdatePostAPI(generics.GenericAPIView):
    permission_classes = [ permissions.IsAuthenticated, IsAuthorOrReadOnly,]
    serializer_class = UpdatePostSerializer

    def get_object(self):
        post_id = self.request.query_params.get('id', None)
        if post_id is not None:
            instance = get_object_or_404(Post, post_id)
        return instance


    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True )
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response({
            "post": PostSerializer(post, context=self.get_serializer_context()).data
            })
# class GetPostDetailView(generics.GenericAPIView):
#     permission_classes = [ permissions.IsAuthenticated, ]
#     serializer_class = UpdatePostSerializer


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

