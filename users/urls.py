from django.urls import path
from users.views import (
    CustomLoginView, CustomLogoutView, RegisterNewUserView,
    RegistrationSuccessfulView, user_profile_view, ChangePasswordView,
    about_the_author_view, get_avatar
)

urlpatterns = [
    path('about', about_the_author_view, name="about"),
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout', CustomLogoutView.as_view(), name="logout"),
    path('register', RegisterNewUserView, name="register"),
    path('registration_successful', RegistrationSuccessfulView, name="registration_successful"),
    path('user_profile', user_profile_view, name="user_profile"),
    path('change_password', ChangePasswordView, name="change_password"),
    path('avatar', get_avatar, name="avatar"),
]