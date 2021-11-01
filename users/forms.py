from typing import Text
from django import forms
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.forms import widgets
from django.forms.widgets import FileInput, TextInput, Widget
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
    """A form to take profile pictures"""
    picture = forms.ImageField(
        label='New Picture :',
        required=False,
        widget=forms.FileInput,
        help_text='- Others can see your profile pic on your posts, comments and profile '
        )
    bio_text = forms.CharField(
        label= 'Bio Text :',
        help_text='You can add up to 150 characters to yor bio .',
        error_messages={'max_length' : 'This bio is more than 150 characters !'},
        required=False,
        widget = forms.TextInput(attrs={'placeholder' : 'Describe Yourslef !'})
    )        
    class Meta :
        model = UserInfo
        fields = ['picture', 'bio_text']
        labels = {'picture' : '', 'bio_text' : ''}