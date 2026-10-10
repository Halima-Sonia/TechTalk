from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from .views import (
    home,
    post_detail,
    category_posts,
    search_posts,
    like_post,
    add_comment,
    create_post,
    edit_post,
    delete_post,
    author_profile,
    discover,
    my_posts,
    bookmark_post,
    my_bookmarks,
    robots_txt,
)

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('', home, name='home'),
    path('create-post/', create_post, name='create_post'),
    path('edit-post/<slug:slug>/', edit_post, name='edit_post'),
    path('delete-post/<slug:slug>/',delete_post,name='delete_post'),
    path('post/<slug:slug>/bookmark/',bookmark_post,name='bookmark_post'),
    path('my-posts/', my_posts, name='my_posts'),
    path('my-bookmarks/',my_bookmarks,name='my_bookmarks'),
    path('post/<slug:slug>/',post_detail,name='post_detail'),
    path('category/<slug:slug>/',category_posts,name='category_posts'),
    path('search/',search_posts,name='search'),
    path('post/<slug:slug>/like/',like_post,name='like_post'),
    path('post/<slug:slug>/comment/',add_comment,name='add_comment'),
    path('author/<str:username>/',author_profile,name='author_profile'),
    path('discover/', discover, name='discover'),
    path('robots.txt',robots_txt,name='robots_txt'),
    path('sitemap.xml',sitemap,{'sitemaps': sitemaps},name='sitemap'),
]