from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('personal/',          views.signup_step1,  name='signup_step1'),
    path('account_creation/',   views.signup_step2,  name='signup_step2'),
    path('contact/',   views.signup_step3,  name='signup_step3'),
    path('profile_image/',   views.signup_step4,  name='signup_step4'),
    path('login/',           views.login,     name='login'),
    path('profile/',         views.profile,        name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', views.delete_account, name='delete_account'),
]