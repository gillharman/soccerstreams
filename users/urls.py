from django.urls import path
from users.views import CustomLoginView, CustomLogoutView, RegisterNewUserView, RegistrationSuccessfulView, UserProfileView

urlpatterns = [
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout', CustomLogoutView.as_view(), name="logout"),
    path('register', RegisterNewUserView, name="register"),
    path('registration_successful', RegistrationSuccessfulView, name="registration_successful"),
    path('user_profile', UserProfileView, name="user_profile")
]