from django.urls import path
from . import views

urlpatterns = [
    path('', views.listPosts, name="home"),
    path('create-post/', views.createPost, name="create-post"),
    path('edit-user/<str:pk>', views.editProfile, name='edit-user'),
    path('signup/', views.registerUser, name="signup"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('search/<str:query>/', views.listPosts, name="search"),
    path('detail/<str:pk>', views.detail, name="detail"),
    path('edit-post/<str:pk>/', views.editPost, name="edit-post"),
    path('delete-post/<str:pk>/', views.deletePost, name="delete-post"),
    path('comment-post/<str:pk>/', views.commentPage, name="comment-post"),
    path('edit-comment/<str:pk>/', views.editComment, name="edit-comment"),
    path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),
    path('profile/<str:pk>/', views.userProfile, name="profile"),
]