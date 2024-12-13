from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
from posts.models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this post.")
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['title', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get posts from users that the current user follows
        user = self.request.user
        followed_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
# @api_view(['POST'])
# def like_post(request, pk):
#     user = request.user
#     post = Post.objects.get(pk=pk)

#     # Check if user already liked the post
#     if Like.objects.filter(user=user, post=post).exists():
#         return Response({"message": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

#     # Create like
#     like = Like.objects.create(user=user, post=post)

#     # Create notification for the post owner
#     notification = Notification.objects.create(
#         recipient=post.user,
#         actor=user,
#         verb="liked your post",
#         target_ct=ContentType.objects.get_for_model(post),
#         target_id=post.id
#     )

#     return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def unlike_post(request, pk):
#     user = request.user
#     post = Post.objects.get(pk=pk)

#     # Check if user has liked the post
#     like = Like.objects.filter(user=user, post=post).first()
#     if not like:
#         return Response({"message": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

#     # Remove like
#     like.delete()

#     return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def like_post(request, pk):
    user = request.user

    # Retrieve the post using get_object_or_404
    post = get_object_or_404(Post, pk=pk)

    # Ensure the user hasn't already liked the post
    like, created = Like.objects.get_or_create(user=user, post=post)

    if not created:
        return Response({"message": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a notification for the post owner when a user likes the post
    Notification.objects.create(
        recipient=post.user,  # The post owner receives the notification
        actor=user,  # The user who liked the post
        verb="liked your post",  # Action description
        target_ct=ContentType.objects.get_for_model(post),  # The content type for Post
        target_id=post.id  # The ID of the liked post
    )

    return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def unlike_post(request, pk):
    user = request.user

    # Retrieve the post using get_object_or_404
    post = get_object_or_404(Post, pk=pk)

    # Check if the user has liked the post
    like = Like.objects.filter(user=user, post=post).first()
    
    if not like:
        return Response({"message": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the like
    like.delete()

    return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)

