# -*- coding: utf-8 -*-

from django.conf.urls import *

from pybb.feeds import LastPosts, LastTopics
from pybb.views import IndexView, CategoryView, ForumView, TopicView,\
    AddPostView, EditPostView, UserView, PostView, ProfileEditView,\
    DeletePostView, StickTopicView, UnstickTopicView, CloseTopicView,\
    OpenTopicView, ModeratePost, TopicPollVoteView, LatestTopicsView, \
    AddWatchAreaView, WatchAreaTopicsView, EditWatchAreaView, \
    DeleteWatchAreaView


urlpatterns = patterns('',
                       # Syndication feeds
                       url('^feeds/posts/$', LastPosts(), name='feed_posts'),
                       url('^feeds/topics/$', LastTopics(), name='feed_topics'),
                       )

urlpatterns += patterns('pybb.views',
                        # Index, Category, Forum
                        url('^$', IndexView.as_view(), name='index'),
                        url('^category/(?P<pk>\d+)/$', CategoryView.as_view(), name='category'),
                        url('^forum/(?P<pk>\d+)/$', ForumView.as_view(), name='forum'),

                        # User
                        url('^users/(?P<username>[^/]+)/$', UserView.as_view(), name='user'),
                        url('^block_user/([^/]+)/$', 'block_user', name='block_user'),

                        # Profile
                        url('^profile/edit/$', ProfileEditView.as_view(), name='edit_profile'),

                        # Topic
                        url('^topic/(?P<pk>\d+)/$', TopicView.as_view(), name='topic'),
                        url('^topic/(?P<pk>\d+)/stick/$', StickTopicView.as_view(), name='stick_topic'),
                        url('^topic/(?P<pk>\d+)/unstick/$', UnstickTopicView.as_view(), name='unstick_topic'),
                        url('^topic/(?P<pk>\d+)/close/$', CloseTopicView.as_view(), name='close_topic'),
                        url('^topic/(?P<pk>\d+)/open/$', OpenTopicView.as_view(), name='open_topic'),
                        url('^topic/(?P<pk>\d+)/poll_vote/$', TopicPollVoteView.as_view(), name='topic_poll_vote'),
                        url('^topic/latest/$', LatestTopicsView.as_view(), name='topic_latest'),

                        # Add topic/post
                        url('^forum/(?P<forum_id>\d+)/topic/add/$', AddPostView.as_view(), name='add_topic'),
                        url('^topic/(?P<topic_id>\d+)/post/add/$', AddPostView.as_view(), name='add_post'),

                        # Post
                        url('^post/(?P<pk>\d+)/$', PostView.as_view(), name='post'),
                        url('^post/(?P<pk>\d+)/edit/$', EditPostView.as_view(), name='edit_post'),
                        url('^post/(?P<pk>\d+)/delete/$', DeletePostView.as_view(), name='delete_post'),
                        url('^post/(?P<pk>\d+)/moderate/$', ModeratePost.as_view(), name='moderate_post'),

                        # Watch areas
                        url('^watch_area/add/$', AddWatchAreaView.as_view(), name='add_watch_area'),
                        url('^watch_area/(?P<pk>\d+)/$', WatchAreaTopicsView.as_view(), name='watch_area_topics'),
                        url('^watch_area/(?P<pk>\d+)/edit/$', EditWatchAreaView.as_view(), name='edit_watch_area'),
                        url('^watch_area/(?P<pk>\d+)/delete/$', DeleteWatchAreaView.as_view(), name='delete_watch_area'),

                        # Attachment
                        #url('^attachment/(\w+)/$', 'show_attachment', name='pybb_attachment'),

                        # Subscription
                        url('^subscription/topic/(\d+)/delete/$',
                            'delete_subscription', name='delete_subscription'),
                        url('^subscription/topic/(\d+)/add/$',
                            'add_subscription', name='add_subscription'),

                        # API
                        url('^api/post_ajax_preview/$', 'post_ajax_preview', name='post_ajax_preview'),

                        # Commands
                        url('^mark_all_as_read/$', 'mark_all_as_read', name='mark_all_as_read')
                        )
