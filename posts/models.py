# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse


class PostVoteCountManager(models.Manager):
    def get_queryset(self):
        return super(PostVoteCountManager, self).get_queryset().annotate(
            votes=Count('vote')).order_by('-points', '-votes')


class Tag(models.Model):
    """ A specific Tag model in the webiste."""
    slug = models.SlugField(max_length=100, unique=True, blank=False)

    def __unicode__(self):
        return self.slug

    class Meta(object):
        verbose_name = "Tag"


class Post(models.Model):
    """A specific Post model in the webiste."""
    title = models.CharField('Title', max_length=100, blank=False)
    author = models.ForeignKey(User, blank=False)
    url = models.URLField('URL', max_length=100, blank=False)
    submitted_on = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    descriptions = models.TextField('Descriptions', max_length=100)
    points = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    # points = models.FloatField(default=0.0)
    with_votes = PostVoteCountManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": str(self.id)})


class Vote(models.Model):
    """ A specific Vote model in the website. """
    voter = models.ForeignKey(User, blank=False)
    post = models.ForeignKey(Post, blank=False)

    def __unicode__(self):
        return "%s voted on %s" % (self.voter.username, self.post.title)


class UserProfile(models.Model):
    """ A specific User Profile model. """
    user = models.OneToOneField(User, unique=True)
    about = models.TextField(null=True)
    website = models.URLField("My website", blank=True, max_length=150)

    def __unicode__(self):
        return "Profil %s" % self.user


def create_profile(**kw):
    user = kw["instance"]
    if kw["created"]:
        up = UserProfile(user=user)
        up.save()


post_save.connect(create_profile, sender=User)