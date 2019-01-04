# -*- coding: utf-8 -*-
# Backend For Newsflash Models built by Adam Sunshine

from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

# Create your models here.
class Author(models.Model):
  """Model Class Representing a User of the App. Extended from the base User class in Django,
  with additions added on such as phone number."""
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone_number = models.CharField(max_length=10)
  # These attributes belong to the user model. Access by _____.user.attribute
  # first_name = models.CharField(max_length=100)
  # last_name = models.CharField(max_length=100)
  # email = models.CharField(max_length=70)

  def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

  def __str__(self):

        return '%s %s' % (self.user.first_name, self.user.last_name)

  def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

class Tag(models.Model):
  """Class representing a topic of news discussion or category. E.g. Sports, Politics, Tech, etc."""
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=500)


  def __str__(self):
        return self.name

  def get_absolute_url(self):
    """
    Returns the url to access a particular tag.
    """
    return reverse('tag-detail', args=[str(self.id)])

class Subtag(models.Model):
  """Class representing a subtopic of news discussion or category. E.g. Tennis, Donald Trump, Ebay, etc."""
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=500)


  def __str__(self):
    return self.name

  def get_absolute_url(self):
      """
      Returns the url to access a particular subtag.
      """
      return reverse('tag-detail', args=[str(self.id)])


class Post(models.Model):
  """Class representing a single post of a news article or story/link. Created by an Author class."""
  title = models.CharField(max_length=100)
  author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
  url = models.URLField(max_length=1000)
  source = models.ForeignKey('Source', on_delete=models.CASCADE, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  tags = models.ManyToManyField(Tag)
  sub_tags = models.ManyToManyField(Subtag)
  is_public = models.BooleanField(default=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
      """
      String for representing the Model object.
      """
      return self.title


  def get_absolute_url(self):
        """
        Returns the url to access a particular post instance.
        """
        return reverse('post-detail', args=[str(self.id)])


class Source(models.Model):
    base_url = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        """
        String representing the source object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular post instance.
        """
        return reverse('source-detail', args=[str(self.id)])