from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from tinymce import models as tinymce_models
class Category(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    short_description = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        help_text="Write a short description about new post! This description will be shown in the main post view!",
    )
    icon = models.TextField(
        null=False,
        blank=False,
        help_text="SVG icon for new category! Write a <svg> HTML tag here...",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Category: {self.title}"

class Post(models.Model):
    
    title = models.CharField(max_length=200, null=False, blank=False)
    short_description = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        help_text="Write a short description about new post! This description will be shown in the main post view!",
    )
    content = tinymce_models.HTMLField(
        null=False, blank=False, help_text="Write a content for your article!"
    )
    image = models.ImageField(
        null=False,
        blank=True,
        help_text="Main post image! We recommend use big image in horizontal layout!",
        upload_to="post_images",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts",
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        """Return average of all comment ratings for this post, or 0."""
        from django.db.models import Avg

        res = self.comments.aggregate(avg=Avg("rating"))
        return res.get("avg") or 0

# Create your models here.

class Comment(models.Model):
    content = models.CharField(max_length=250, null=False, blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", null=False, blank=False
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", null=False, blank=False
    )
    rating = models.PositiveIntegerField(
        null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    