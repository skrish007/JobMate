from . import views
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('login', views.login_view, name='login'),
    path('userdash', views.success_view, name='userdash'),
    path('companydash', views.success_view, name='companydash'),
    path('admindash', views.success_view, name='admindash'),
    
    path('register',views.register,name='register'),
    path('companyreg',views.companyreg,name='companyreg'),
    path('logout', views.logout_view, name='logout'),
    path('seekerpro', views.seekerpro, name='seekerpro'),

    # URL pattern for the 'seeker_profile_update' view
    path('seeker_profile_update', views.seeker_profile_update, name='seeker_profile_update'),
    path('providerpro', views.providerpro, name='providerpro'),

    path('provider_profile_update', views.provider_profile_update, name='provider_profile_update'),
    path('verification_pending', views.verification_pending, name='verification_pending'),
    
    path('ad',views.admin,name='ad'),
    path('postjob', views.post_job, name='postjob'),
    path('seekerlist', views.seekerlist, name='seekerlist'),
    path('companydash', views.seekerview, name='companydash'),
    path('companylist', views.companylist, name='companylist'),
    path('viewpostedjobs', views.posted_jobs, name='viewpostedjobs'),
    path('job/<int:job_id>/', views.viewjobdetails, name='viewjobdetails'),
    path('companylist', views.savecompanies, name='savecompanies'),

    #---------------Change pw------------------------------
    
    path('changepw_seeker', views.changepw_seeker, name='changepw_seeker'),
    path('changepw_pro', views.changepw_pro, name='changepw_pro'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('verifymail', views.verifymail, name='verifymail'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('companyjobs', views.companyjobs, name='companyjobs'),
    path('edit_job/<int:job_id>', views.edit_job, name='edit_job'),

    path('updatestatus/<int:job_id>', views.companyjobs, name='edit_job'),
    path('delete_job/<int:job_id>', views.delete_job, name='delete_job'),
    
    path('accounts/', include('allauth.urls')),
]


    