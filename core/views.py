from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

from core.models import Post
from users.models import FavouritePosts

def index(request):
    from .models import Post, Category
    from django.db.models import Avg
    
    posts = Post.objects.order_by("-created_at").all()
    categories = Category.objects.order_by("-created_at").all()
    
    top_post=Post.objects.annotate(avg_rating=Avg("comments__rating")).order_by("-avg_rating").first()
    
    return render(
        request, "index.html", {"posts": posts[0:5], "categories": categories, "top_post":top_post}
    )

def all_posts(request):
    from .models import Post
    from .models import Category
    from django.db.models import Q
    from django.core.paginator import Paginator

    query = request.GET.get("search", "")
    posts = Post.objects.order_by("-created_at").all()
        
    category_id = request.GET.get("category_id", "")
    categories = Category.objects.all()


    
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(content__icontains=query)
            | Q(category__title__icontains=query)
            | Q(author__username__icontains=query)
        )

    if category_id:
        category=Category.objects.filter(id=category_id).first()
        
        if category:
            category_id = int(category_id)
            posts = posts.filter(category=category)

    # Пагінація - 10 постів на сторінку
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)

    return render(request, "all_posts.html", {"posts": page_obj, "categories": categories, "query": query, "page_obj": page_obj, "category_id": int(category_id) if category_id else None})

def about_us(request):
    from .models import Post
    return render(request, "About_us.html", {"posts": about_us})




def post_detail(request, post_id):
    from .models import Post
    from django.shortcuts import get_object_or_404
    from .forms import CommentForm
     


    post = get_object_or_404(Post, id=post_id)
    posts_by_category = Post.objects.filter(category=post.category).exclude(id=post.id).all()
    print(post)
    comments = post.comments.all().order_by('-created_at').all()


    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if not request.user.is_authenticated:
            next_url = request.get_full_path()
            login_url = f"{reverse("login")}?next={next_url}"
            
            return redirect(login_url)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    is_favourite = False
    if request.user and request.user.is_authenticated:
        is_favourite = FavouritePosts.objects.filter(
            user=request.user, post=post
        ).exists()
    return render(request, 'post_detail.html', {'post': post, 'posts_by_category': posts_by_category[0:3], 'form': form, 'comments': comments, 'is_favourite': is_favourite})

def post_creation(request):
    from .forms import PostForm

    form = PostForm(request.POST or request.GET)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("all_posts")

        
    return render(request, "create_post.html", {"form": form})

def delete_comment(request, comment_id):
    from .models import Comment
    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse,HttpResponse
    if request.method == "DELETE":
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return JsonResponse({"error": "You are not authorized to delete this comment."}, status=400)
        comment.delete()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "Method not allowed."}, status=405)
    
@login_required
def edit_post(request, post_id):
    from .forms import PostForm
    from .models import Post
    from django.shortcuts import redirect, get_object_or_404
    from django.http import Http404
    
    post=get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        raise Http404("No Post found with current id!")

    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():

            form.save()

            return redirect("post_detail", post_id=post.id)

    return render(request, "create_post.html", {"form": form})

@login_required
def delete_post(request, post_id):
    from django.shortcuts import get_object_or_404
    from .models import Post
    from django.http import JsonResponse, HttpResponse

    if request.method == "DELETE":
        post = get_object_or_404(Post, id=post_id)

        if post.author != request.user:
            return JsonResponse(
                {"error": "Only comment author can delete it!"}, status=400
            )

        post.delete()

        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)