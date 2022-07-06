from rest_framework import serializers
from .models import User, UserLoggedInSession

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    

class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({
                "password": "Both password should match"
            })
        if User.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError({
                "username": "username already taken"
            })
        return super().validate(attrs)
    
    

class UserOutSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = [
            'username',
            'first_name',
            'last_name',
            
        ]
    

class UserLoggedinSessionOutSerializer(serializers.ModelSerializer):

    class Meta:
        model  = UserLoggedInSession
        exclude = [
            'user',
            'access_token',
            'refresh_token',
        ]
    