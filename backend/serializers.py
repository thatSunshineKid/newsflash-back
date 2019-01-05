from rest_framework import serializers, generics
from .models import Post, Author
from django.contrib.auth.models import User


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


class CreateAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','password',)
        extra_kwargs = {'password': {'write_only': True}}


    def create(self,validated_data):
      #create user and create author
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password']
                                        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        author = Author.objects.create(user=user)

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ('id', 'first_name', 'last_name', 'username')


