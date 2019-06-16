from django.urls import path
from users.views import CustomLoginView

urlpatterns = [
    path('login', CustomLoginView.as_view(), name="login")
]