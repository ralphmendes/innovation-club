from django.conf.urls import url
from .views import (
    CreatePost,
    DetailPost,
    DraftPosts,
    UpdatePost,
    DeletePost,
    post_publish,
    add_comment,
    vote_post,
)

app_name = 'blog'
urlpatterns = [
    url(r'posts/(?P<pk>\d+)/publish/$',post_publish,name='post_publish'),
    url(r'^create/$',CreatePost.as_view(),name='create'),
    url(r'^detail/(?P<pk>\d+)/$',DetailPost.as_view(),name='detail'),
    url(r'^drafts/$',DraftPosts.as_view(),name='draft'),
    url(r'^update/(?P<pk>\d+)/$',UpdatePost.as_view(),name='update'),
    url(r'^delete/(?P<pk>\d+)/$',DeletePost.as_view(),name='delete'),
    url(r'^post/(?P<pk>\d+)/comment/$', add_comment, name='add_comment'),
    url(r'^post/(?P<pk>\d+)/vote/(?P<vote_type>\-?\d+)/$', vote_post, name='vote_post'),
]
