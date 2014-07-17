# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib import admin

admin.autodiscover()

from posts.views import PostListView, UserProfileDetailView, \
    UserProfileEditView, PostCreateView, PostDetailView, PostEditView, \
    PostDeleteView, VoteFormView, PostListAllView


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PostListView.as_view(), name='home'),
    url(r'^zakopalisko/$', PostListAllView.as_view(), name='lounge'),
    url(r'^login/$', "django.contrib.auth.views.login",
        {"template_name": "registration/login.html"}, name="login"),
    url(r'^logout/$',
        "django.contrib.auth.views.logout_then_login", name="logout"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^users/(?P<slug>\w+)/$',
        UserProfileDetailView.as_view(), name='profile'),
    url(r'^edit_profile/$',
        login_required(UserProfileEditView.as_view()), name='edit_profile'),
    url(r'^post/create/$',
        login_required(PostCreateView.as_view()), name='create_post'),
    url(r'^post/(?P<pk>\d+)$',
        PostDetailView.as_view(), name='post_detail'),
    url(r'^post/edit/(?P<pk>\d+)$',
        login_required(PostEditView.as_view()), name='post_edit'),
    url(r'^post/delete/(?P<pk>\d+)$',
        login_required(PostDeleteView.as_view()), name='post_delete'),
    url(r'^vote/$', login_required(VoteFormView.as_view()), name="vote"),
)

