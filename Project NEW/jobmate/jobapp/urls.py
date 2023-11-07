from . import views
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('',views.home),
    path('home',views.home),
    path('login', views.login_view, name='login'),
    path('userdash', views.success_view, name='userdash'),
    path('companydash', views.success_view, name='companydash'),
    path('admindash', views.success_view, name='admindash'),
    path('userdash', views.success_view, name='userdash'),
    path('register',views.register),
    path('companyreg',views.companyreg),
    path('logout', views.logout_view, name='logout'),
    path('seekerpro', views.seekerpro, name='seekerpro'),

    # URL pattern for the 'seeker_profile_update' view
    path('seeker_profile_update', views.seeker_profile_update, name='seeker_profile_update'),
    path('providerpro', views.providerpro, name='providerpro'),

    path('provider_profile_update', views.provider_profile_update, name='provider_profile_update'),
    path('verification_pending', views.verification_pending, name='verification_pending'),
    
    path('ad',views.admin,name='ad'),
    path('postjob', views.PostJob, name='postjob'),
    path('seekerlist', views.seekerlist, name='seekerlist'),
    path('companylist', views.companylist, name='companylist'),
    
]

from django.contrib.auth.views import LoginView
    