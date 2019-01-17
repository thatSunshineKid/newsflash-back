from rest_framework import serializers, generics
from .models import Post, Author, Source, Tag, Subtag
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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

class CreatePostSerializer(serializers.ModelSerializer):
    #create arrays of strings for tags and subtags to quickly see if they exist or not
    tags = serializers.ListField(child=serializers.CharField(), )
    sub_tags = serializers.ListField(child=serializers.CharField(), )
    class Meta:
        model = Post
        fields = ('title','url','tags','sub_tags','is_public')


    def create(self,validated_data):
        #handle capture of user/author object, source from url, create tag/subtag objects
        #and create post
        author = self.context['request'].user.author
        url = validated_data['url'].split("/")
        if url[2]:
            slug = url[2]
        else:
            slug = url[0]
        try:
            match = Source.objects.get(base_url=slug)
        except Source.DoesNotExist:
            match = None
        if match:
            val_source = match
        else:
            val_source = Source.objects.create(base_url=slug, title=slug.split(".")[1])
        tag_list = []
        stag_list = []
        #go through and iterate over tags list and create/attach them as we go through
        for tag in validated_data['tags']:
            try:
                tname = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                tname = None
            if tname:
                tag_list.append(tname)
            else:
                tname = Tag.objects.create(name=tag, description="to be added by management soon.")
                tag_list.append(tname)
            tname = None
        #same things for sub_tags, iterate through and create/attach subtag objects
        for s_tag in validated_data['sub_tags']:
            try:
                sname = Subtag.objects.get(name=s_tag)
            except Subtag.DoesNotExist:
                sname = None
            if sname:
                stag_list.append(sname)
            else:
                sname = Subtag.objects.create(name=s_tag, description="to also be added by management soon.")
                stag_list.append(sname)
            sname = None
        post = Post.objects.create(author=author, title=validated_data['title'],
                                    url=validated_data['url'],
                                    source=val_source,
                                    is_public= bool(validated_data['is_public']),
                                    )
        for t in tag_list:
            post.tags.add(t)
        for s in stag_list:
            post.sub_tags.add(s)
        post.save()
        return post

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
      fields = ('id', 'first_name', 'last_name', 'username', 'email')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")

