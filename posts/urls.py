from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),  # Filter posts by a category
    path('post/<slug:post_slug>/', views.post_detail, name='post_detail'),  # reading a full post
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('create/', views.post_create, name='post_create'),
    path('edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('liked-posts/', views.liked_posts, name='liked_posts'),
]
