from django import forms
from django.forms import widgets
from django.forms.fields import FileField, ImageField
from django.forms.widgets import FileInput, 
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
    """A form to take profile pictures"""
    class Meta :
        model = UserInfo
        fields = ['picture', 'bio_text']
        labels = {'picture' : '', 'bio_text' : ''}
        widgets = {'name' : ImageField(widget=FileInput)}