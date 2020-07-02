from rest_framework import serializers

from social_network.network.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class PostLikeSerializerCreate(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PostLike
        fields = '__all__'


class PostLikeSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        exclude = ('post', 'user')

    def validate(self, data):
        """
        Validate authenticated user
        """

        if self.instance.user != self.context['request'].user:
            raise serializers.ValidationError('You can not edit post votes from other users')
        return data

class PostLikeSerializerAnalytics(serializers.ModelSerializer):
    create_date = serializers.DateField(
        read_only=True
    )
    id_count = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = PostLike
        fields = ('post_id', 'create_date', 'id_count')
        depth = 1
