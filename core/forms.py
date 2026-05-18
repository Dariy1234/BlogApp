from django.forms import ModelForm
from django import forms
from .models import Post
from .models import Comment
from tinymce.widgets import TinyMCE

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "short_description", "content", "image", "category"]
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["rating", "content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your comment..."}
            ),
            "rating": forms.HiddenInput()
        }
