from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), many=True, read_only=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'comments']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=False)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post', 'timestamp')