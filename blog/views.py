from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Like, Comment, Bookmark
from account.models import Profile
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils.text import slugify
from .forms import PostForm
from django.contrib.auth.models import User


def discover(request):
    return render(request, 'discover.html')

def home(request):

    posts = Post.objects.filter(
        is_published=True
    ).annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comments', distinct=True)
    ).order_by('-created_at')

    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    # Trending posts
    trending_posts = Post.objects.filter(
        is_published=True
    ).annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comments', distinct=True)
    ).order_by(
        '-like_count',
        '-comment_count',
        '-created_at'
    )[:3]

    return render(request, 'home.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'trending_posts': trending_posts
    })


def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True
    )

    return render(request, 'post_detail.html', {
        'post': post
    })


def category_posts(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    posts = Post.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')

    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'category.html', {
        'category': category,
        'posts': page_obj,
        'page_obj': page_obj
    })



def search_posts(request):

    query = request.GET.get('q', '').strip()

    posts = Post.objects.filter(
        is_published=True
    )

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()

    posts = posts.order_by('-created_at')

    return render(request, 'search.html', {
        'posts': posts,
        'query': query
    })


# =========================
# Like / Unlike
# =========================

@login_required
def like_post(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if like:
        like.delete()

    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect('post_detail', slug=post.slug)

# =========================
# Bookmark / Unbookmark
# =========================

@login_required
def bookmark_post(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True
    )

    bookmark = Bookmark.objects.filter(
        user=request.user,
        post=post
    ).first()

    if bookmark:
        bookmark.delete()
    else:
        Bookmark.objects.create(
            user=request.user,
            post=post
        )

    return redirect('post_detail', slug=post.slug)

@login_required
def my_bookmarks(request):

    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related('post').order_by('-created_at')

    return render(request, 'my_bookmarks.html', {
        'bookmarks': bookmarks
    })

# =========================
# Add Comment
# =========================

@login_required
def add_comment(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True
    )

    if request.method == 'POST':

        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )

    return redirect('post_detail', slug=post.slug)


@login_required
def create_post(request):

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            # Automatically set the author
            post.author = request.user

            # Automatically create slug from title
            post.slug = slugify(post.title)

            post.save()

            return redirect('post_detail', slug=post.slug)

    else:
        form = PostForm()

    return render(request, 'create_post.html', {
        'form': form
    })

@login_required
def edit_post(request, slug):

    post = get_object_or_404(Post, slug=slug)

    # Only the author can edit the post
    if post.author != request.user:
        return redirect('post_detail', slug=post.slug)

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()

            return redirect('post_detail', slug=post.slug)

    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {
        'form': form,
        'post': post
    })

@login_required
def delete_post(request, slug):

    post = get_object_or_404(Post, slug=slug)

    # Only the author can delete the post
    if post.author != request.user:
        return redirect('post_detail', slug=post.slug)

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'delete_post.html', {
        'post': post
    })

@login_required
def my_posts(request):

    posts = Post.objects.filter(
        author=request.user
    ).order_by('-created_at')

    return render(request, 'my_posts.html', {
        'posts': posts
    })

def author_profile(request, username):

    author = get_object_or_404(User, username=username)

    posts = Post.objects.filter(
        author=author,
        is_published=True
    ).order_by('-created_at')

    profile, created = Profile.objects.get_or_create(
        user=author
    )

    return render(request, 'author_profile.html', {
        'author': author,
        'profile': profile,
        'posts': posts,
    })


def robots_txt(request):

    return render(
        request,
        'robots.txt',
        content_type='text/plain'
    )