# authapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    #Extra
    path('',views.landing, name='Landing'),
    path('services/',views.services, name='services'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('login_Dash/',views.loginDash, name='login_Dash'),
    #Ended
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('otp/', views.verify_otp_view, name='verify_otp'),
]
