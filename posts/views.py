from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from . models import Post, Comment
from . forms import PostForm, CommentForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


#######################################
##         comment section           ##
#######################################

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)




#######################################
##         Api section           ##
#######################################
import json
import requests


def post_list(request):
    post_List_api_call = requests.get("https://jsonplaceholder.typicode.com/posts")
    try:
        posts=json.loads(post_List_api_call.content)
    except Exception as e:
        posts= "error"
    return render(request, 'blog-listing.html', {'posts':posts})


def post_details(request, *args, **kwargs):
    post_id = kwargs.get("post_id")

    post_detail_api_call = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    comment_api_call = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments")
    try:
        post_detail = json.loads(post_detail_api_call.content)
        comments = json.loads(comment_api_call.content)
    except Exception as e:
        post_detail = "error"
        comments = "error"

    return render(request, 'blog-post.html',{'post':post_detail, 'comments':comments})
