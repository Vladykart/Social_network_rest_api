from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

from .views import PostView, PostDetail, PostLikeView, PostLikeDetail, PostLikeAnalytics

from .views import UserView, UserDetail

urlpatterns = [
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-auth/', obtain_jwt_token),

    # Users
    url(r'^users$', UserView.as_view()),
    url(r'^users/(?P<user_id>[\d]+)$', UserDetail.as_view()),

    # Posts
    url(r'^posts$', PostView.as_view()),
    url(r'^posts/(?P<post_id>[\d]+)$', PostDetail.as_view()),

    # Post Likes
    url(r'^post_likes$', PostLikeView.as_view()),
    url(r'^post_likes/(?P<post_vote_id>[\d]+)$', PostLikeDetail.as_view()),
    # url(r'^analytics$', PostLikeAnalytics.as_view()),
    #Analytics
    url('^analytics/(?P<date_from>\d{4}-\d{2}-\d{2})/(?P<date_to>\d{4}-\d{2}-\d{2})$',
        PostLikeAnalytics.as_view()),
]
