from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Avg, Count

from users.models import FavouritePosts
def registration(request):
    from .forms import RegistrationForm
    from .models import Profile
    form=RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile=Profile(user=user)
            profile.save()
            print("Registration success:", user)

            return redirect("login")

    return render(request, 'regitration.html',{'form':form})

def login_view(request):
    from .forms import LoginForm
    from django.contrib.auth import authenticate, login

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.POST.get("next") or request.GET.get("next")
                is_secure = url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                )
                print("Next url: ", next_url, "Is secure: ", is_secure)
                if next_url and is_secure:
                    return redirect(next_url)
                else:
                    return redirect("index")
                

    return render(request, "login.html", {"form": form})

@login_required
def logout(request):
    from django.contrib.auth import logout

    logout(request)

    return redirect("login")

@login_required
def profile(request, username=None):
    from django.contrib.auth.models import User
    from django.shortcuts import get_object_or_404
    from core.models import Post

    user = get_object_or_404(User, username=username) if username else request.user
    # annotate posts with average rating so template can render it efficiently
    user_posts = (
        Post.objects.filter(author=user)
        .annotate(avg_rating=Avg("comments__rating"))
        .order_by("-created_at")
    )
    user_comments = user.comments.all().order_by("-created_at")
    favourite_posts = FavouritePosts.objects.filter(user=user).all()
    # figure out average rating across all comments on this user's posts
    author_rating_data = (
        user_comments.filter(post__author=user)
        .aggregate(avg=Avg("rating"))
    )
    author_avg_rating = author_rating_data.get('avg') or 0
    subscribers_count = user.subscribers.count()
    context = {
        'profile_user': user,
        'user_posts': user_posts,
        'user_comments': user_comments,
        'posts_count': user_posts.count(),
        'comments_count': user_comments.count(),
        'favourite_posts': favourite_posts,
        'author_avg_rating': author_avg_rating,
        'subscribers_count': subscribers_count,
    }
    
    return render(request, 'profile.html', context)



@login_required
def toggle_favourite_post(request, post_id):
    from django.http import JsonResponse
    from .models import FavouritePosts
    from core.models import Post
    from django.shortcuts import get_object_or_404

    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "error": "Forbidden. Use method POST!"}, status=405
        )

    post = get_object_or_404(Post, id=post_id)
    favourite = FavouritePosts.objects.filter(user=request.user, post=post).first()
    if favourite:
        favourite.delete()
        return JsonResponse({"status": "removed"}, status=200)

    favourite = FavouritePosts(user=request.user, post=post)
    favourite.save()

    return JsonResponse({"status": "saved"}, status=201)


@login_required
def edit_profile(request):
    from django.http import JsonResponse
    from django.contrib.auth.models import User

    if request.method != "POST":
        return JsonResponse({"status": "error", "error": "POST only"}, status=405)

    user = request.user

    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()

    if username and username != user.username:
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"status": "error", "error": "Username already taken"}, status=400
            )

        user.username = username

    if email and email != user.email:
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"status": "error", "error": "Email already taken"}, status=400
            )

        user.email = email

    user.save()

    profile = user.profile
    bio = request.POST.get("bio", "").strip()

    if bio and bio != profile.bio:
        profile.bio = bio

    if "avatar" in request.FILES:
        profile.profile_picture = request.FILES["avatar"]

    profile.save()

    return JsonResponse(
        {
            "status": "success",
            "user": {
                "username": user.username,
                "email": user.email,
                "bio": profile.bio,
                "avatar": profile.profile_picture.url if profile.profile_picture else None,
            },
        }
    )  
    

@login_required
def toggle_subscription(request, author_id):
    from django.http import JsonResponse
    from .models import Subscription

    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "error": "Forbidden. Use method POST!"}, status=405
        )

    author = get_object_or_404(User, id=author_id)

    if author == request.user:
        return JsonResponse(
            {"status": "error", "error": "You can not subscribe to yourself!"},
            status=400,
        )

    sub = Subscription.objects.filter(subscriber=request.user, author=author).first()
    if sub:
        sub.delete()
        return JsonResponse({"status": "unsubscribed"}, status=200)
    else:
        Subscription.objects.create(subscriber=request.user, author=author)
        return JsonResponse({"status": "subscribed"}, status=201)
