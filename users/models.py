from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from core.models import Post

class FavouritePosts(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="favourite_posts",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="in_favourites",
    )

    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        null=False,
        blank=False,
    )
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "author"], name="unique_subscriptions"
            )
        ]

    def __str__(self):
        return f"{self.subscriber.username} => {self.author.username}"