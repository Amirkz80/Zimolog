from typing import AbstractSet
from django import forms
from django.forms.widgets import TextInput
from .models import BlogPost,Comments

class BlogPostForm(forms.ModelForm):
    """A class to make forms for posts"""
    title = forms.CharField(
        required= False,
        help_text= 'You can add up to 100 characters to the title .',
        widget = forms.TextInput(attrs={'placeholder' : 'This part is optional to fill'})
    )
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

class EmailSharingForm(forms.Form):
    """A form to share posts via email"""
    name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    send_to = forms.EmailField(required=True)
    comment = forms.CharField(required=False, widget=forms.Textarea)

        