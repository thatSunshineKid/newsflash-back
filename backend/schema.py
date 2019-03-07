# cookbook/ingredients/schema.py
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


class Query(object):
    all_posts = graphene.List(PostType)
    all_sources = graphene.List(SourceType)
    all_authors = graphene.List(AuthorType)
    user = graphene.Field(UserType)
    author = graphene.Field(AuthorType)
    me = graphene.Field(AuthorType)
    my_posts = graphene.List(PostType)

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




class Mutation(object):
    create_author = CreateAuthor.Field()



