from rest_framework import serializers, generics
from .models import Post, Author


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
