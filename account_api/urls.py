from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView
urlpatterns = [
    path('register',UserRegistrationView.as_view()),
    path('login',UserLoginView.as_view()),
    # path('profile',UserProfileView.as_view()),
    path('change-password',UserChangePasswordView.as_view()),
    path('reset-password',SendPasswordResetEmailView.as_view()),
    path('reset-password/<uid>/<token>',UserPasswordResetView.as_view())

]
