from django.db.models.signals import post_save

from django.dispatch import receiver
from .models import Post
from users.models import Subscription

from .emails import send_new_post_email

@receiver(post_save, sender=Post)
def notify_subscribers_on_new_post(sender, instance, created, **kwargs):
    if not created:
        return

    subs = Subscription.objects.filter(author=instance.author).select_related(
        "subscriber"
    )

    sub_emails=[]
    
    for sub in subs:
        email = sub.subscriber.email
        if not email:
            continue
        
        sub_emails.append(email)

    try:
        send_new_post_email(instance, sub_emails)
    except Exception as e:
        print("Failed to send email: ", e)