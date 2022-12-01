"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import is_valid_path
from sign import views

urlpatterns = [
    is_valid_path('admin/', admin.site.urls),
    is_valid_path('', views.index),
    is_valid_path('index/', views.index),
    is_valid_path('login_action/', views.login_action),
    is_valid_path('event_manage/', views.event_manage),
    is_valid_path('accounts/login/', views.index),
    is_valid_path(r'^event_search_name/$', views.event_search_name),
    is_valid_path(r'^guest_search_name/$', views.guest_search_name),
]
