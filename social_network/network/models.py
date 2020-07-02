import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from .managers import constants
from .managers.user_manager import UserManager


# from django.contrib.auth.models import User


class User(AbstractBaseUser, PermissionsMixin):
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    last_login = models.DateTimeField(default=None, blank=True, null=True)
    last_request = models.DateTimeField(default=None, blank=True, null=True)
    # token = models.CharField(max_length=300)
    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'network'

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = str(uuid.uuid4()).replace('-', '')
        super(User, self).save(*args, **kwargs)


class Post(models.Model):
    STATUS = (
        (0, "Draft"),
        (1, "Publish")
    )

    # slug = models.SlugField(max_length=200, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        default_related_name = 'posts'
        ordering = ['-created_on']

    def __str__(self):
        return self.content


class Like(TimeStampedModel):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.DO_NOTHING, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             related_name='likes',
                             on_delete=models.CASCADE, )
    liked_date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(choices=constants.VOTE_VALUE_CHOICES)

    class Meta:
        abstract = True

    def __str__(self):
        return '{} from {}'.format(self.post, self.user)


class PostLike(Like):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, )

    class Meta:
        default_related_name = 'post_likes'
        unique_together = ('post', 'user')

    def __str__(self):
        return f'post: {self.post.id} - value: {self.value}'


class CreatedModified(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
