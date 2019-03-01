from rest_framework import serializers, generics
from drf_writable_nested import WritableNestedModelSerializer
from .models import Post, Author, Source, Tag, Subtag
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

class TagSerializer(serializers.ModelSerializer):
    detail_link = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='tag-detail')
    class Meta:
        model = Tag
        fields = ('name','description','id', 'detail_link')

class SubtagSerializer(serializers.ModelSerializer):
    detail_link = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='subtag-detail')
    class Meta:
        model = Subtag
        fields = ('name','description','id', 'detail_link')


class SourceSerializer(serializers.ModelSerializer):
    detail_link = serializers.HyperlinkedRelatedField(many=False,read_only=True, view_name='source-detail')
    class Meta:
        model = Source
        fields = ('base_url','title','id','detail_link')

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    detail_link = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='author-detail')
    class Meta:
        model = Author
        fields = ('user', 'detail_link')

class PostSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(many=False)
    # tags = serializers.SlugRelatedField(
    #   many=True,
    #   read_only=True,
    #   slug_field='name'
    #   )
    tags = TagSerializer(many=True)
    # source = serializers.SlugRelatedField(
    #   many=False,
    #   read_only=True,
    #   slug_field='title'
    #   )
    sub_tags = SubtagSerializer(many=True)
    source = SourceSerializer(many=False)
    # sub_tags = serializers.SlugRelatedField(
    #   many=True,
    #   read_only=True,
    #   slug_field='name'
    #   )
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

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")

class FindOrCreateTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Tag
        fields = ('pk','name',)

    def create(self, validated_data):
        try:
            find_obj = Tag.objects.get(name__like=validated_data['name'])
        except Tag.DoesNotExist:
            find_obj = None
        if find_obj:
            return find_obj
        else:
            return Tag.objects.create(name=validated_data['name'], description='admin coming soon.')

class FindOrCreateSubtagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Subtag
        fields = ('pk','name',)

    def create(self, validated_data):
        try:
            find_obj = Subtag.objects.get(name__like=validated_data['name'])
        except Subtag.DoesNotExist:
            found_obj = None
        if found_obj:
            return found_obj
        else:
            return Subtag.objects.create(name=validated_data['name'], description='admin coming soon yep.')

class FindOrCreateSourceSerializer(serializers.ModelSerializer):
    url = serializers.CharField()
    class Meta:
        model = Tag
        fields = ('pk','url',)

    def create(self, validated_data):
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
            return match
        else:
            return Source.objects.create(base_url=slug, title=slug.split(".")[1])

class UpdatePostSerializer(WritableNestedModelSerializer):
    tags = FindOrCreateTagSerializer(many=True)
    subtags = FindOrCreateSubtagSerializer(many=True)
    source = FindOrCreateSourceSerializer(many=False)
    class Meta:
        model = Post
        fields = ('pk','title','url','is_public','tags','subtags','source')

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        stags = validated_data.pop('subtags')
        source = validated_data.pop('source')
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.is_public = validated_data.get('is_public')
        tag_set = list(instance.tags.all())
        stag_set = list(instance.sub_tags.all())
        source_set = list(instance.source)
        for tag in tags:
            n_tag = tag_set.pop(0)
            n_tag.name = tag.get('name', n_tag.name)
            n_tag.description = tag.get('description', n_tag.description)
            n_tag.save()
        for stag in tsags:
            s_tag = stag_set.pop(0)
            s_tag.name = stag.get('name', s_tag.name)
            s_tag.description = stag.get('description', s_tag.description)
            s_tag.save()
        # for v_tag in validated_data.get('tags'):
        #     instance.tags.add(v_tag)
        # for s_tag in validated_data.get('subtags'):
        #     instance.subtags.add(s_tag)
        instance.source = validated_data.get('source')
        instance.save()
        return instance

#--------NEW STUFF -------------------------------------

class SimpleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name','description')

class SimpleSubtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtag
        fields = ('id','name','description')

class SimpleSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id','base_url','title')


# class SimplePostSerializer(WritableNestedModelSerializer):
#     add_tags = SimpleTagSerializer(many=True)
#     add_subtags = SimpleSubtagSerializer(many=True)
#     remove_tags = SimpleTagSerializer(many=True, null=True)
# #     remove_subtags = SimpleSubtagSerializer(many=True, null=True)

# #update create and update with add_tags and subtags /remove :)
#     class Meta:
#         model = Post
#         fields = ('id','title','url','is_public','add_tags','add_subtags','remove_tags','remove_subtags')

    # def create(self,validated_data):

    #     #grab author and tags/subtags data for creation of object
    #     author = self.context['request'].user.author
    #     tags = validated_data.pop('add_tags')
    #     stags = validated_data.pop('add_subtags')
    #     #process post url and auto grab source object
    #     url_data = validated_data['url'].split("/")
    #     if url_data[2]:
    #         slug = url_data[2]
    #     else:
    #         slug = url_data[0]
    #     try:
    #         match = Source.objects.get(base_url=slug)
    #     except Source.DoesNotExist:
    #         match = None
    #     if match:
    #         true_source = match
    #     else:
    #         true_source = Source.objects.create(base_url=slug, title=slug.split(".")[1])
    #     for tag in tags:
    #         try:
    #             tname = Tag.objects.get(id=tag.get('id'))
    #         except Tag.DoesNotExist:
    #             try:
    #                 tname = Tag.objects.get(name=tag.get('name'))
    #             except Tag.DoesNotExist:
    #                 tname = Tag.objects.create(name=tag, description="to be added by management soon.")
    #         if tname:
    #             tag_list.append(tname)
    #         else:
    #             break
    #     #same things for sub_tags, iterate through and create/attach subtag objects
    #     for s_tag in validated_data['sub_tags']:
    #         try:
    #             sname = Subtag.objects.get(id=s_tag.get('id'))
    #         except Subtag.DoesNotExist:
    #             try:
    #                 sname = Subtag.objects.get(name=s_tag.get('name'))
    #             except Subtag.DoesNotExist:
    #                 sname = Subtag.objects.create(name=tag, description="to be added by management soon.")
    #         if sname:
    #             stag_list.append(sname)
    #     post = Post.objects.create(author=author, title=validated_data['title'],
    #                                 url=validated_data['url'],
    #                                 source=val_source,
    #                                 is_public= bool(validated_data['is_public']),
    #                                 )
    #     for t in tag_list:
    #         post.tags.add(t)
    #     for s in stag_list:
    #         post.sub_tags.add(s)
    #     post.save()
    #     return post
    #         #see if ID is in data - if so tag already exists

    # def update(self, instance, validated_data):
    #     tags = validated_data.pop('add_tags')
    #     subtags = validated_data.pop('add_subtags')
    #     r_tags = validated_data.pop('remove_tags')
    #     r_stags = validated_data.pop('remove_subtags')
    #     existing_tags = instance.tags.all()
    #     existing_subtags = instance.subtags.all()
    #     existing_tags = list(existing_tags)
    #     existing_subtags = list(existing_subtags)
    #     existing_source = instance.source
    #     existing_source = list(existing_source)

    #     url_data = validated_data['url'].split("/")
    #     if url_data[2]:
    #         slug = url_data[2]
    #     else:
    #         slug = url_data[0]
    #     try:
    #         match = Source.objects.get(base_url=slug)
    #     except Source.DoesNotExist:
    #         match = None
    #     if match:
    #         true_source = match
    #     else:
    #         true_source = Source.objects.create(base_url=slug, title=slug.split(".")[1])
    #     tag_list = []
    #     stag_list = []
    #     #find/create tag and subtags object models
    #     for tag in tags:
    #         if tag.get('id'):
    #              try:
    #                 add = Tag.objects.get(id=tag.get('id'))

    #     for t in tag_list:
    #         tag = existing_tags.pop(0)

#use these simple serializers to create a nested Post serializer for Creating and Updating Posts.



