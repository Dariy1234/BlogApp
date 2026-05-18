from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from django.conf import settings

from django.urls import reverse

def send_new_post_email(post: Post, follower_email: list[str]):
    site_url = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")

    post_url = site_url + reverse("post_detail", args=[post.id])
    image_url = None

    if post.image:
        image_url = site_url + post.image.url

    html_content = render_to_string(
        "new_post.html",
        context={"post": post, "post_url": post_url, "image_url": image_url},
    )

    subject = f"New post by {post.author.username.title()}: {post.title.title()}"

    msg = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=follower_email,
        headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()