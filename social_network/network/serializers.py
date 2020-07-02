from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from .likes.like_serializers import PostLikeSerializer
from .models import Post, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id']


class UserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    @staticmethod
    def validate_password(password):
        """
        Validate password
        """

        validate_password(password)
        return password


class UserSerializerLogin(UserSerializer):
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user):
        """
        Get or create token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'token')


class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class PostSerializer(serializers.ModelSerializer):
    # post_reply_count = serializers.SerializerMethodField()
    post_like = PostLikeSerializer(many=True, read_only=True)
    user = UserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user',)

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit posts from other users')
        return data
