from django import forms
from .models import BlogPost,Comments

class BlogPostForm(forms.ModelForm):
    """A class to make forms for posts"""
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {'title': 'Post Title', 'text': 'Text' }
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class CommentsForm(forms.ModelForm):
    """A class to make forms for new comments"""
    class Meta:
        model = Comments
        fields = ['text']
        labels = {'text' : ''}
        widgets = {'text': forms.Textarea(attrs={'cols' : 80})}