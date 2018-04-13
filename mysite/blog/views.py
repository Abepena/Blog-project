from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from blog.forms import PostForm, CommentForm

from django.views.generic import (TemplateView, ListView,
                                    DetailView,CreateView,
                                    UpdateView, DeleteView,)
# Create your views here.

###############################
######      POSTS   ###########
###############################

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    # Define how to grab the ListView
    """get_queryset does a query like a SQL query on my models
    Grabs the Post model, all the objects in it, then filters out by the
    conditions stated after .filter grabs the published_date ... __lte = less
    than or equal to the time right now and orders them ascending or descending
    based on the - or nothing preceding what is placed inside of order_by
    method"""

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    """
    mixins to be used like decorators in function based views
    the login_url and redirect_field_name attributes are Login Required mixins
    that redirect the user to the blog/post_detail page when creating a Post view after
    requiring a login
    """

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):

    """
    Updating an existing view instead of creating a new one
    """

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


###############################
######      COMMENTS   ########
###############################

@login_required # convenience decorator that requires user to be logged in to comment
def add_comment_to_post(request, pk):

    post = get_object_or_404(Post, pk = pk) #gets post of primary key 'pk' object or gives a 404 error

    if request.method == 'POST':
        form = CommentForm(request.POST)    #grabs the data posted
        if form.is_valid():
            comment = form.save(commit=False) #creates a form called comment but does not commit data
            comment.post = post #Comment model has an attribute called post that is a foreign key. This makes that foreign key equal to the post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()

    return render(request,'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve() # in models.py the approved_comment attribute is default False but this method sets that BooleanField to True
    return redirect('post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk #need to save the post primary key in order to return it in the redirect
    comment.delete()
    return redirect('post_detail', pk = post_pk)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish
    redirect('post_detail',pk = 'pk')
