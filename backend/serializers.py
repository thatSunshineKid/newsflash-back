from rest_framework import serializers, generics
from .models import Post, Author


class PostSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(many=False)
    tags = serializers.SlugRelatedField(
      many=True,
      read_only=True,
      slug_field='name'
      )
    source = serializers.SlugRelatedField(
      many=False,
      read_only=True,
      slug_field='title'
      )
    sub_tags = serializers.SlugRelatedField(
      many=True,
      read_only=True,
      slug_field='name'
      )



    class Meta:
        model = Post
        fields = ('id','author','title','url','source','tags','sub_tags','created_at','is_public')
