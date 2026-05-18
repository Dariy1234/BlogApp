from django.urls import path


from .views import *


urlpatterns = [
    path("", index,name="index"),
    path("posts/", all_posts, name="all_posts"),
    path("about_us/", about_us, name="about_us"),
    
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('create_post/', post_creation, name='post_creation'),
    path("posts/comments/<int:comment_id>/", delete_comment, name="delete_comment"),
    path("posts/<int:post_id>/edit/", edit_post, name="edit_post"),
    path("posts/<int:post_id>/delete/", delete_post, name="delete_post"),
    
]

