from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .forms import CreatePostForm
from django.contrib.auth.models import User
from users.models import Poster
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseNotFound

def home(request):
    p = False
    if request.user.is_anonymous:
        p = False
    else:
        poster = Poster.objects.filter(user=request.user)
        if poster.exists():
            p = poster.first().Permissive_to_post
        else:
            p = False
    posts_list = Post.objects.all().order_by('-date_posted')
    page = request.GET.get('page',1)
    paginator = Paginator(posts_list,5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'can_post': p
    }
    return render(request, 'blog/home.html', context)

def user_posts(request, pk):
    p = False
    if request.user.is_anonymous:
        p = False
    else:
        poster = Poster.objects.filter(user=request.user)
        if poster.exists():
            p = poster.first().Permissive_to_post
        else:
            p = False
    u_list = User.objects.filter(pk = pk).all()
    if not u_list.exists():
        return HttpResponseNotFound("<h1>404!NotFound</h1>")
    u = u_list.first()    
    posts_list = Post.objects.filter(author=u).all().order_by('-date_posted')
    page = request.GET.get('page',1)
    paginator = Paginator(posts_list,5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'can_post': p
    }
    return render(request, 'blog/user_posts.html', context)

def topic_posts(request, topic):
    p = False
    if request.user.is_anonymous:
        p = False
    else:
        poster = Poster.objects.filter(user=request.user)
        if poster.exists():
            p = poster.first().Permissive_to_post
        else:
            p = False
    p_list = Post.objects.filter(category = topic).all()
    if not p_list.exists():
        return HttpResponseNotFound("<h1>404!NotFound</h1>")
    posts_list = p_list.order_by('-date_posted')
    page = request.GET.get('page',1)
    paginator = Paginator(posts_list,5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'can_post': p
    }
    return render(request, 'blog/topic_posts.html', context)

@login_required
def create_post(request):
    p = False
    want_to_be_poster = False
    if request.user.is_anonymous:
        p = False
    else:
        poster = Poster.objects.filter(user=request.user)
        if poster.exists():
            p = poster.first().Permissive_to_post
            if p == False:
                want_to_be_poster = True
        else:
            p = False
    if p == False:
        if want_to_be_poster:
            messages.warning(request,f'You can not post yet!Wait for admin permission!')
        else:
            messages.warning(request,f'You can not post!Beacause you are not a poster!')
        return redirect('blog-home')
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f'Your Post is created!You can see it in home page!')
            return redirect('blog-home')
    else:
        form = CreatePostForm()
    return render(request,'blog/post_form.html',{'form': form, 'can_post': p})

class PostDetailView(DetailView):
    model = Post
    can_post = False
    post_obj = Post()

    def get(self, request, *args, **kwargs):
        context = locals()
        if self.request.user.is_anonymous:
            self.can_post = False
        else:
            poster = Poster.objects.filter(user=self.request.user)
            if poster.exists():
                self.can_post = poster.first().Permissive_to_post
            else:
                self.can_post = False
        context['can_post'] = self.can_post
        context['post_obj'] = Post.objects.filter(pk=kwargs['pk']).first()
        return render(request, 'blog/post_detail.html', context)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        can_post = False
        if self.request.user.is_anonymous:
            can_post = False
        else:
            poster = Poster.objects.filter(user=self.request.user)
            if poster.exists():
                can_post = poster.first().Permissive_to_post
            else:
                can_post = False
        context['can_post'] = can_post
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        can_post = False
        if self.request.user.is_anonymous:
            can_post = False
        else:
            poster = Poster.objects.filter(user=self.request.user)
            if poster.exists():
                can_post = poster.first().Permissive_to_post
            else:
                can_post = False
        context['can_post'] = can_post
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    p = False
    if request.user.is_anonymous:
        p = False
    else:
        poster = Poster.objects.filter(user=request.user)
        if poster.exists():
            p = poster.first().Permissive_to_post
        else:
            p = False
    return render(request, 'blog/about.html', {'title': 'About','can_post': p})