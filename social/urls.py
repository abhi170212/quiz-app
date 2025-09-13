from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('upvote/<str:username>/', views.toggle_upvote, name='toggle_upvote'),
    path('comment/<str:username>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
]