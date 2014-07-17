# coding=utf-8
from django.forms import ModelForm
from models import UserProfile, Post, Vote


class UserProfileForm(ModelForm):
    class Meta(object):
        model = UserProfile
        exclude = ("user", )


class PostForm(ModelForm):
    class Meta(object):
        #todo widget for tags
        model = Post
        exclude = ("points", "author", "tags", )


class VoteForm(ModelForm):
    class Meta(object):
        model = Vote
