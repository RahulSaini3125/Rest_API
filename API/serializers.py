from rest_framework import serializers
from .models import *

class BlogModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModels
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length= 20, write_only= True)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CategoryModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModels
        fields = "__all__"

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EmailAvailabilitySerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserAboutYouUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['aboutYou']

class EmailAvailabilitySerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerificationSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_profile']