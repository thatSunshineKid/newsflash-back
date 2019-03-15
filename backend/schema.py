
import graphene
import graphql_jwt
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType

from .models import *


class PostType(DjangoObjectType):
    class Meta:
        model = Post

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author

class SourceType(DjangoObjectType):
    class Meta:
        model = Source

class UserType(DjangoObjectType):
    class Meta:
        model = User

class TagType(DjangoObjectType):
    class Meta:
        model = Tag

class SubtagType(DjangoObjectType):
    class Meta:
        model = Subtag

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String(required=True)
        url = graphene.String(required=True)
        tags = graphene.List(graphene.String)
        subtags = graphene.List(graphene.String)
        is_public = graphene.Boolean()
        description = graphene.String()

    def mutate(self, info, title, url, tags, subtags, is_public, description, base_url=None):
        #build the post object from these arguments. copy from before logic
        #KISS
        user = info.context.user
        if user.is_anonymous:
            raise Exception('not logged in!')
        else:
            author = user.author
            lurl = url.split("/")
            if lurl[2]:
                dom = lurl[2]
            else:
                dom = lurl[0]
            try:
                match = Source.objects.get(base_url=dom)
            except Source.DoesNotExist:
                match = Source.objects.create(base_url=dom, title=dom)
            t_l = []
            st_l= []
            for t in tags:
                try:
                    a_t = Tag.objects.get(name=t)
                except Tag.DoesNotExist:
                    a_t = Tag.objects.create(name=t, description="added via quickadd from %s." % (author))
                t_l.append(a_t)
                a_t = None
            for s in subtags:
                try:
                    a_st = Subtag.objects.get(name=s)
                except Subtag.DoesNotExist:
                    a_st = Subtag.objects.create(name=s, description="added via quickadd from %s." % (author))
                st_l.append(a_st)
                a_st = None
            post = Post.objects.create(author=author, title=title, url=url, source=match, is_public=is_public, description=description)
            for x in t_l:
                post.tags.add(x)
            for y in st_l:
                post.sub_tags.add(y)
            post.save()
        return CreatePost(post=post)

class EditPost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.Int(required=True)
        title = graphene.String()
        url = graphene.String()
        add_tags = graphene.List(graphene.String)
        remove_tags = graphene.List(graphene.String)
        add_subtags = graphene.List(graphene.String)
        remove_subtags = graphene.List(graphene.String)
        is_public = graphene.Boolean()
        description = graphene.String()

    def mutate(self, info, post_id, title, url, add_tags, remove_tags, add_subtags, remove_subtags, is_public, description):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('not logged in!')
        else:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                raise Exception('No post found with id %s' % (post_id))
            if (post.author.id != user.author.id):
                raise Exception('only the author can edit their own posts')
            else:
                post.title = title
                post.is_public = is_public
                post.description = description
                if (url == post.url):
                    z = 1
                else:
                    post.url = url
                    if (post.source.base_url == url.split("/")[ 2 if url.split("/")[2] else 0 ]):
                        pass
                    else:
                        dom = url.split("/")[ 2 if url.split("/")[2] else 0 ]
                        try:
                            a_s = Source.objects.get(base_url=dom)
                        except Source.DoesNotExist:
                            a_s = Source.objects.create(base_url=dom, title=dom)
                        post.source = a_s
                for t in add_tags:
                    try:
                        a_t = Tag.objects.get(name=t)
                    except Tag.DoesNotExist:
                        raise Exception('create Tag from Edit Post is not supported. Please create tag %s first and then add it to this post.' % (t))
                    post.tags.add(a_t)
                    a_t = None
                for s in add_subtags:
                    try:
                        s_t = Subtag.objects.get(name=s)
                    except Subtag.DoesNotExist:
                        raise Exception('create Subtag from Edit Post is not supported. Please create subtag %s first and then add it to this post.' % (s))
                    post.sub_tags.add(s_t)
                    s_t = None
                for x in remove_tags:
                    try:
                        x_t = Tag.objects.get(name=x)
                    except Tag.DoesNotExist:
                        raise Exception('tag no exist!')
                    if x_t in post.tags.all():
                        post.tags.remove(x_t)
                        x_t = None
                    else:
                        raise Exception('this tag %s is not attached to this post.' % (x_t))
                for y in remove_subtags:
                    try:
                        y_s = Subtag.objects.get(name=y)
                    except Subtag.DoesNotExist:
                        raise Exception('subtag no exist!')
                    if y_s in post.sub_tags.all():
                        post.sub_tags.remove(y_s)
                        y_s = None
                    else:
                        raise Exception('this subtag %s is not attached to this post.' % (y_s))
                post.save()
                return EditPost(post)

class CreateAuthor(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        firstname = graphene.String(required=True)
        lastname = graphene.String(required=True)
        phonenumber = graphene.String(required=False)

    def mutate(self, info, username, password, email, firstname, lastname, phonenumber):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        author = Author.objects.create(user=user, phone_number=phonenumber)

        return CreateAuthor(user=user)

class CreateTag(graphene.Mutation):
    tag = graphene.Field(TagType)
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
    def mutate(self, info, name, description):
        tag = Tag.objects.create(name=name, description=description)
        return CreateTag(tag)

class CreateSubtag(graphene.Mutation):
    subtag = graphene.Field(SubtagType)
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
    def mutate(self,info, name, description):
        subtag = Subtag.objects.create(name=name, description=description)
        return CreateSubtag(subtag)

class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)
    class Arguments:
        post_id = graphene.Int(required=True)
        message = graphene.String(required=True)
    def mutate(self, info, post_id, message):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Exception('No post found with id %s' % (post_id))
        user = info.context.user
        if user.is_anonymous:
            raise Exception('not logged in!')
        else:
            comment = Comment.objects.create(author=user.author, post=post, message=message, is_public=True)
            return CreateComment(comment)

class Query(object):
    all_posts = graphene.List(PostType)
    all_sources = graphene.List(SourceType)
    all_authors = graphene.List(AuthorType)
    user = graphene.Field(UserType)
    author = graphene.Field(AuthorType)
    source = graphene.Field(SourceType)
    me = graphene.Field(AuthorType)
    my_posts = graphene.List(PostType)
    all_tags = graphene.List(TagType)
    all_subtags = graphene.List(SubtagType)
    comments = graphene.List(CommentType)

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_all_sources(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Source.objects.all()

    def resolve_all_authors(self, info, **kwargs):
        return Author.objects.all()

    def resolve_user(self, info, **kwargs):
        return Author.user

    def resolve_author(self, info, **kwargs):
        return User.author

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        else:
            return user.author

    def resolve_my_posts(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        else:
            return Post.objects.filter(author = user.author)

    def resolve_all_tags(self, info):
        return Tag.objects.all()

    def resolve_all_subtags(self, info):
        return Subtag.objects.all()


    def resolve_source(self, info):
        return Post.source

    def resolve_comments(self, info):
        return Post.comments.all()

class Mutation(object):
    create_author = CreateAuthor.Field()
    create_post = CreatePost.Field()
    create_tag = CreateTag.Field()
    create_subtag = CreateSubtag.Field()
    create_comment = CreateComment.Field()
    edit_post = EditPost.Field()



