from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import User
from rest_framework.views import APIView

# For follow and unfollow functionality, we use these views.
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        # Ensure the user is not following themselves
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the 'following' list
        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        # Ensure the user is not trying to unfollow themselves
        if user_to_unfollow == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user from the 'following' list
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)


class UserListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        """
        Retrieve all users except the current user.
        """
        users = User.objects.exclude(id=request.user.id)  # Exclude the current user
        user_data = [{"id": user.id, "username": user.username} for user in users]
        return Response(user_data)


class FeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get all the posts from the users that the current user follows
        followed_users = request.user.following.all()
        posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')  # Get posts from followed users

        # Serialize the posts
        post_data = [{"id": post.id, "content": post.content, "created_at": post.created_at, "user": post.user.username} for post in posts]
        
        return Response(post_data)








# from django.contrib.auth import authenticate
# from rest_framework import status, permissions
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .serializers import UserSerializer, LoginSerializer
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404
# from accounts.models import User


# class FollowUserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id):
#         # Get the user to follow
#         user_to_follow = get_object_or_404(User, id=user_id)
#         if user_to_follow == request.user:
#             return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Follow the user
#         request.user.following.add(user_to_follow)
#         return Response({"detail": f"Followed {user_to_follow.username}"}, status=status.HTTP_200_OK)

# class UnfollowUserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id):
#         # Get the user to unfollow
#         user_to_unfollow = get_object_or_404(User, id=user_id)
#         if user_to_unfollow == request.user:
#             return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Unfollow the user
#         request.user.following.remove(user_to_unfollow)
#         return Response({"detail": f"Unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)

# class RegisterView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = authenticate(
#                 username=serializer.validated_data['username'],
#                 password=serializer.validated_data['password']
#             )
#             if user:
#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key}, status=status.HTTP_200_OK)
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
