from . import views
from django.urls import path

urlpatterns = [
    path('',views.home),
    path('home',views.home),
    path('login', views.login_view, name='login'),
    path('userdash', views.success_view, name='userdash'),
    path('companydash', views.success_view, name='companydash'),
    path('userdash', views.success_view, name='userdash'),
    path('register',views.register),
    path('companyreg',views.companyreg),
    path('logout', views.logout_view, name='logout'),
    
]

from django.contrib.auth.views import LoginView
