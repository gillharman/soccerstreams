from django.urls import path
from users.views import (
    CustomLoginView, CustomLogoutView, register_new_user_view,
    registration_successful_view, user_profile_view, ChangePasswordView,
    about_the_author_view, get_avatar
)

urlpatterns = [
    path('about', about_the_author_view, name="about"),
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout', CustomLogoutView.as_view(), name="logout"),
    path('register', register_new_user_view, name="register"),
    path('registration_successful', registration_successful_view, name="registration_successful"),
    path('user_profile', user_profile_view, name="user_profile"),
    path('change_password', ChangePasswordView.as_view(), name="change_password"),
    path('avatar', get_avatar, name="avatar"),
]