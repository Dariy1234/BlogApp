from django.contrib import admin
from .models import Profile, FavouritePosts, Subscription

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["bio", "user__username"]
    autocomplete_fields = ["user"]
    readonly_fields = ["created_at", "updated_at"]

@admin.register(FavouritePosts)
class FavouritePostsAdmin(admin.ModelAdmin):
    list_display = ["user", "post__title", "created_at"]
    list_filter = ["user", "created_at"]
    search_fields = ["user", "post__title", "post__short_description"]
    autocomplete_fields = ["user", "post"]
    readonly_fields = ["created_at"]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["subscriber", "author", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["subscriber__username", "author__username"]
    autocomplete_fields = ["subscriber", "author"]
    readonly_fields = ["created_at"]
