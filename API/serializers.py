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