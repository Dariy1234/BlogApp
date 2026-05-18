from django.contrib import admin
from .models import Post
from .models import Category    
from django.utils.html import format_html
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at"]
    fields = ["title", "short_description", "icon", "icon_preview", "created_at"]
    search_fields = ["title", "short_desctiption"]
    list_filter = [
        "created_at",
    ]
    date_hierarchy = "created_at"
    ordering = [
        "-created_at",
    ]
    readonly_fields = [
        "icon_preview",
        "created_at",
        
    ]
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(obj.icon)
        else:
            return "No category icon!"
    # format_html("<img src={}>", obj.image.url)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "created_at"]
    search_fields = ["title", "short_description" "content"]
    list_filter = [
        "category",
        "created_at",
    ]
    date_hierarchy = "created_at"
    ordering = [
        "-created_at",
    ]
    readonly_fields = [
        "image_preview",
        "created_at",
    ]

    

    fields = [
        "title",
        "short_description",
        "content",
        "author",
        "category",
        "image",
        "image_preview",
        "created_at",

    ]

    

    def image_preview(self, obj):
        if obj.image:
            return format_html("<img src='{}' width='300' />", obj.image.url)
        else:
            return "No image!"
        
