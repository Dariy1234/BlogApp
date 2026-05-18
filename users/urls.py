from django.urls import path
from .views import *

urlpatterns = [
    path("registration/", registration, name="registration"),
    path("login/", login_view, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/<str:username>/", profile, name="profile"),
    path(
        "posts/<int:post_id>/favourite/toggle",
    
    
        toggle_favourite_post,
        name="toggle_favourite_post",
    ),
    
    path("profile/my/edit/", edit_profile, name="edit_profile"),
    path("authors/<int:author_id>/subscription/toggle/", toggle_subscription, name="toggle_subscription"),




























    
]

# Create your urls here.