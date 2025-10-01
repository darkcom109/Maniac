from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your insult here...'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Leave a reply...'}),
        }
