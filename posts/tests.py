from django.test import TestCase
from django.contrib.auth import get_user_model
from models import Post, Tag


class PostModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")

    def test_require_fields(self):
        post = Post()
        self.assertRaises(Exception, post.save, title="")


class TagModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")

    def test_require_fields(self):
        tag = Tag()
        self.assertRaises(Exception, tag.save, slug="")