from dataclasses import fields
from rest_framework import serializers
from blogs.models import User
from users.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    """A serializer class to serialize userinfo model"""   
    
    class Meta:
        model = UserInfo
        fields = ['followers_number', 'following_number', 'followers', 'following', 'bio_text', 'picture']

class UserSerializer(serializers.ModelSerializer):
    """A class to serialize User model"""

    userinfo = UserInfoSerializer()    
    
    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'is_authenticated', 'is_active', 'userinfo']