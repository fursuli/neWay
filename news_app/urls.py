from django.contrib import admin
from django.shortcuts import redirect
from django.urls import re_path
from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache

from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    re_path(r'^ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),
    re_path(r'^signUp/$', views.signup, name='signUp'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
    re_path(r'^users/$', views.UserListView.as_view(), name='users'),
    re_path(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user-details'),
    re_path(r'^news/$', views.ApprovedPostListView.as_view(), name='approved'),
    re_path(r'^news/not-approved/$', views.NotApprovedPostListView.as_view(), name='not_approved'),
    re_path(r'^news/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post-details'),
    re_path(r'^news/create/$', views.create_post, name='creating-news'),

    re_path(r'^news/(?P<pk>\d+)/add-comment/$', views.add_comment_to_post, name='add_comment_to_post'),
]
