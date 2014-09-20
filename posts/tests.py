# coding=utf-8
from django.core.urlresolvers import NoReverseMatch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .models import Post, Tag, UserProfile, Vote


class PostModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")
        self.post = Post(title="new title", author=self.user,
                         url="http://example.net")

    def test_require_fields(self):
        post = Post()
        self.assertRaises(Exception, post.save, title="")

    def test_return_created_user_profile(self):
        post = Post(title="new title", author=self.user,
                    url="http://example.net")
        self.assertEqual("new title", post.__str__())
        self.assertEqual("new title", post.__unicode__())

    def test_get_absolute_url(self):
        pass


class TagModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")

    def test_require_fields(self):
        tag = Tag()
        self.assertRaises(Exception, tag.save, slug="")

    def test_return_created_user_profile(self):
        tag = Tag(slug=slugify(u"Test Nowego Taga"))
        self.assertEqual("test-nowego-taga", tag.__str__())
        self.assertEqual("test-nowego-taga", tag.__unicode__())


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")

    def test_create_user_profile(self):
        user_profiles = (
            UserProfile(user=self.user),
            UserProfile(user=self.user, website="http://o2.pl/"),
            UserProfile(user=self.user, website="http://o2.pl/",
                        about="info..."))

        self.assertEqual("testuser", user_profiles[0].user.__str__())
        self.assertEqual("", user_profiles[0].website)
        self.assertEqual(None, user_profiles[0].about)

        self.assertEqual("testuser", user_profiles[1].user.__str__())
        self.assertEqual("http://o2.pl/", user_profiles[1].website)
        self.assertEqual(None, user_profiles[1].about)

        self.assertEqual("testuser", user_profiles[2].user.__str__())
        self.assertEqual("http://o2.pl/", user_profiles[2].website)
        self.assertEqual("info...", user_profiles[2].about)

    def test_return_created_user_profile(self):
        up = UserProfile(user=self.user)
        self.assertEqual("Profil testuser", up.__str__())
        self.assertEqual("Profil testuser", up.__unicode__())


class VoteModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")
        self.post = Post(title="My new post", url="http://example.net",
                         descriptions="Test descrtiptions...")

    def test_create_vote(self):
        vote = Vote(voter=self.user, post=self.post)
        self.assertEqual("testuser voted on My new post", vote.__str__())

