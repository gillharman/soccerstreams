from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, HttpResponse

from .forms import customAuthForm, customUserCreationForm, UserProfileForm
from .models import User

# Create your views here.

class CustomLoginView(LoginView):
    form_class = customAuthForm
    template_name = 'login.html'
    extra_context = {
        "data": {
            "next": "/"
        }
    }


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'


def RegisterNewUserView(request):
    if request.method == "POST":
        form = customUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            return redirect("/users/registration_successful")

    else:
        form = customUserCreationForm()

    return render(request, 'register.html',
                  {"data": {
                          "form": form,
                  }})


def RegistrationSuccessfulView(request):
    return render(request, 'registration_successful.html')


def user_profile_view(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            # user.avatar = form.cleaned_data["avatar"]
            user.save()

    user = User.objects.get(id=request.user.id)
    form = UserProfileForm(instance=user)

    return render(request, "user_profile.html",
                  { "data": {
                      "user": user,
                      "form": form,
                  }})


def ChangePasswordView(request):
    pass