from . import views
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import path, include

urlpatterns = [
    path('',views.home),
    path('home',views.home),
    path('login', views.login_view, name='login'),
    path('userdash', views.success_view, name='userdash'),
    path('companydash', views.success_view, name='companydash'),
    path('admindash', views.success_view, name='admindash'),
    
    path('register',views.register),
    path('companyreg',views.companyreg),
    path('logout', views.logout_view, name='logout'),
    path('seekerpro', views.seekerpro, name='seekerpro'),
    
    # URL pattern for the 'seeker_profile_update' view
    path('seekerupdate', views.seeker_profile_update, name='seekerupdate'),
    path('providerpro', views.providerpro, name='providerpro'),

    path('provider_profile_update', views.provider_profile_update, name='provider_profile_update'),
    path('verification_pending', views.verification_pending, name='verification_pending'),
    
    path('ad',views.admin,name='ad'),
    path('postjob', views.post_job, name='postjob'),
    path('seekerlist', views.seekerlist, name='seekerlist'),
    path('companylist', views.companylist, name='companylist'),
    path('viewpostedjobs', views.posted_jobs, name='viewpostedjobs'),
    path('companylist', views.savecompanies, name='savecompanies'),

    #---------------Change pw------------------------------
    
    path('changepw_seeker', views.changepw_seeker, name='changepw_seeker'),
    path('changepw_pro', views.changepw_pro, name='changepw_pro'),







]


    