from django import forms
from django.forms.widgets import FileInput
from .models import UserInfo

class UserInfoForm(forms.ModelForm):
    """A form to take profile pictures"""
    picture = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta :
        model = UserInfo
        fields = ['picture', 'bio_text']
        labels = {'picture' : '', 'bio_text' : ''}