
from django.urls import path 
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView

urlpatterns = [

    path("register/",UserRegistrationView.as_view()),
    path("login/",UserLoginView.as_view()),
    path("profile/",UserProfileView.as_view()),
    path("changepassword/",UserChangePasswordView.as_view()),
    path("send-reset-password-email/",SendPasswordResetEmailView.as_view()),
    path("reset-password/<uid>/<token>/",UserPasswordResetView.as_view()),
   

]
