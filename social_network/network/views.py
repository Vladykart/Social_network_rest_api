# from rest_framework.generics import GenericAPIView
# from rest_framework_tracking.mixins import LoggingMixin
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import DateField, Count, Sum
from django.db.models.functions import Cast



from .likes.like_serializers import PostLikeSerializerUpdate, PostLikeSerializer, PostLikeSerializerCreate, \
    PostLikeSerializerAnalytics
from .models import Post, PostLike, User

from .serializers import UserSerializer, PostSerializer, PostSerializerCreate, PostSerializerUpdate, \
    UserSerializerLogin, UserSerializerCreate, UserSerializerUpdate



# users
class UserView(APIView):

    @staticmethod
    def get(request):
        """
        List users
        """

        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    @staticmethod
    def post(request):
        """
        Create user
        """

        serializer = UserSerializerCreate(data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# users/{user_id}
class UserDetail(APIView):

    @staticmethod
    def get(request, user_id):
        """
        View individual user
        """

        user = get_object_or_404(User, pk=user_id)
        return Response(UserSerializer(user).data)

    @staticmethod
    def patch(request, user_id):
        """
        Update authenticated user
        """

        user = get_object_or_404(User, pk=user_id)
        if user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializerUpdate(user, data=request.data,
                                          context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializerLogin(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# posts
class PostView(APIView):

    @staticmethod
    def get(request):
        """
        List posts
        """

        posts = Post.objects.all()
        # posts = post_filter(request, posts)
        if type(posts) == Response:
            return posts
        return Response(PostSerializer(posts, many=True).data)

    @staticmethod
    def post(request):
        """
        Create post
        """

        serializer = PostSerializerCreate(data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(PostSerializer(serializer.instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# posts/{post_id}
class PostDetail(APIView):

    @staticmethod
    def get(request, post_id):
        """
        View individual post
        """

        post = get_object_or_404(Post, pk=post_id)
        return Response(PostSerializer(post).data)

    @staticmethod
    def patch(request, post_id):
        """
        Update post
        """

        post = get_object_or_404(Post, pk=post_id)
        serializer = PostSerializerUpdate(post, data=request.data,
                                          context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PostSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, post_id):
        """
        Delete post
        """

        post = get_object_or_404(Post, pk=post_id)
        if post.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# post_likes
class PostLikeView(APIView):

    @staticmethod
    def post(request):
        """
        Create post like
        """

        serializer = PostLikeSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(PostLikeSerializer(serializer.instance).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


# post_likes/{post_vote_id}
class PostLikeDetail(APIView):

    @staticmethod
    def patch(request, post_vote_id):
        """
        Update post vote
        """

        post_vote = get_object_or_404(PostLike, pk=post_vote_id)
        serializer = PostLikeSerializerUpdate(post_vote, data=request.data,
                                              context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PostLikeSerializer(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, post_vote_id):
        """
        Delete post vote
        """

        post_vote = get_object_or_404(PostLike, pk=post_vote_id)
        if post_vote.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        post_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeAnalytics(APIView):
    @staticmethod
    def get(request, date_from, date_to):
        """
        View filtered liked posts
        """

        print()
        query = PostLike.objects.filter(
            created__gte=date_from,
            created__lte=date_to
        ).annotate(
            create_date=Cast('created', DateField())
        ).values('create_date', 'post_id').annotate(
            id_count=Sum('value')
        ).order_by('create_date')
        print(query)
        return Response(PostLikeSerializerAnalytics(query, many=True).data)
