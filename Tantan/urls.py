"""Tantan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from UserApp import apis as user_api
from SocialApp import apis as social_api

from home import views

urlpatterns = [
    # user模块
    path('api/user/vcode/fetch', user_api.fetch_code),
    path('api/user/vcode/submit', user_api.submit_code),
    path('api/user/profile/show', user_api.show_profile),
    path('api/user/profile/update', user_api.update_profile),
    path('qiniu/token', user_api.qn_token),
    path('qiniu/callback', user_api.qn_callback),

    # social模块
    path('api/social/rcmd', social_api.rcmd_users),
    path('api/social/like', social_api.like),
    path('api/social/superlike', social_api.super_like),
    path('api/social/dislike', social_api.dislike),
    path('api/social/rewind', social_api.rewind),
    path('api/social/fans', social_api.fans),
    path('api/social/friends', social_api.friends),
    path('api/social/rank', social_api.hot_rank),


    # 前端页面--首页
    path('', views.index),

]
