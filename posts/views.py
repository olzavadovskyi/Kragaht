from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostForm


def category_posts(request, category_slug):  # Display posts that belong to a specific category.

    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category_id=category.pk)
    categories = Category.objects.all()
    return render(request, 'posts/category_posts.html', {'category': category, 'categories': categories, 'posts': posts})


def my_posts(request):
    categories = Category.objects.all()
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        user_posts = Post.objects.filter(author=request.user)
        return render(request, 'posts/my_posts.html', {'posts': user_posts, 'categories': categories})


def post_list(request):
    query = request.GET.get('q')  # Search query
    sort_by = request.GET.get('sort', 'time_create')

    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()
    # sorting
    if sort_by == 'name':
        posts = posts.order_by('title')
    elif sort_by == 'likes':
        posts = posts.annotate(like_count=Count('likes')).order_by('-like_count')
    elif sort_by == 'time_create':
        posts = posts.order_by('-time_create')

    for post in posts:
        post.user_liked = request.user.is_authenticated and post.likes.filter(id=request.user.id).exists()

    categories = Category.objects.all()

    return render(request, 'posts/post_list.html', {
        'posts': posts, 'categories': categories, 'query': query, 'sort_by': sort_by,
    })


def post_detail(request, post_slug):  # full post
    post = get_object_or_404(Post, slug=post_slug)
    similar_posts = Post.objects.exclude(id=post.id)[:5]  # give 5 similar posts
    categories = Category.objects.all()
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'similar_posts': similar_posts,
        'categories': categories,
    })


def liked_posts(request):
    categories = Category.objects.all()
    if not request.user.is_authenticated:
        return redirect('login')

    liked_posts = Post.objects.filter(likes=request.user)
    return render(request, 'posts/liked_posts.html', {'posts': liked_posts, 'categories': categories})


def toggle_like(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({'liked': liked, 'like_count': post.get_like_count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def post_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form, 'form_title': 'Create Post', 'categories': categories})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_staff:
        return redirect('posts:post_list')  # Redirect unauthorized users
    categories = Category.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'categories': categories})


@login_required
def post_delete(request, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_staff:
        return redirect('posts:post_list')
    if request.method == 'POST':
        post.delete()
        return redirect('posts:post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'posts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('posts:post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'posts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('posts:post_list')
