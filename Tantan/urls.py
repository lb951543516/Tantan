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
from UserApp import apis

urlpatterns = [
    # user模块
    path('api/user/vcode/fetch/', apis.fetch_code),
    path('api/user/vcode/submit/', apis.submit_code),
    path('api/user/profile/show/', apis.show_profile),
    path('api/user/profile/update/', apis.update_profile),
    path('qiniu/token/', apis.qn_token),
    path('qiniu/callback/', apis.qn_callback),
]
