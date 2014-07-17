# coding=utf-8
import json
from django.db.models import Count

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, \
    DeleteView, FormView
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, reverse_lazy

from models import Post, UserProfile, Vote
from forms import UserProfileForm, PostForm, VoteForm

number_votes_to_main = 1


class PostListView(ListView):
    model = Post
    queryset = Post.with_votes.annotate(count=Count('vote')).exclude(
        count__lt=number_votes_to_main)
    paginate_by = 5
    template_name = "posts/post_list.html"

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = Vote.objects.filter(voter=self.request.user)
            links_in_page = [link.id for link in context["object_list"]]
            voted = voted.filter(post_id__in=links_in_page)
            voted = voted.values_list('post_id', flat=True)
            context["voted"] = voted
        return context


class PostListAllView(ListView):
    model = Post
    # queryset = Post.with_votes.all()
    queryset = Post.with_votes.annotate(count=Count('vote')).exclude(
        count__gte=number_votes_to_main)

    paginate_by = 5
    template_name = "posts/post_list_all.html"

    def get_context_data(self, **kwargs):
        context = super(PostListAllView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            voted = Vote.objects.filter(voter=self.request.user)
            posts_in_page = [post.id for post in context["object_list"]]
            voted = voted.filter(post_id__in=posts_in_page)
            voted = voted.values_list('post_id', flat=True)
            context["voted"] = voted
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_post.html"

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.points = 0
        f.save()
        return super(PostCreateView, self).form_valid(form)


class PostDetailView(DetailView):
    model = Post


class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_post.html"


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("home")


class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "posts/user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user


class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "posts/edit_profile.html"

    # bierzemy tylko obiekt naszego zalogowanego człowieka
    def get_object(self, query=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={"slug": self.request.user})


class JSONForm(object):
    @staticmethod
    def create_response(vdict=None, valid_form=True):
        if not vdict:
            vdict = dict()
        response = HttpResponse(
            json.dumps(vdict),
            content_type='application/json'
        )
        response.status = 200 if valid_form else 500
        return response


class VoteFormBaseView(FormView):
    form_class = VoteForm

    @staticmethod
    def create_response(vdict=None, valid_form=True):
        if not vdict:
            vdict = dict()
        response = HttpResponse(
            json.dumps(vdict),
            content_type='application/json'
        )
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=form.data["post"])
        user = self.request.user
        prev_vote = Vote.objects.filter(voter=user, post=post)
        has_voted = (prev_vote.count() > 0)

        ret = {"success": 1}
        if not has_voted:
            # add vote
            v = Vote.objects.create(voter=user, post=post)
            ret["voteobj"] = v.id
        else:
            # delete vote
            prev_vote[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret)

    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors}
        return self.create_response(ret, False)


class VoteFormView(VoteFormBaseView, JSONForm):
    pass
