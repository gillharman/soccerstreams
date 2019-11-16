from django.shortcuts import render, redirect, HttpResponse
from .forms import customAuthForm, customUserCreationForm, UserProfileForm
from django.contrib.auth.views import LoginView, LogoutView

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


def UserProfileView(request):
    form = UserProfileForm()
    print(form)
    return render(request, "user_profile.html",
                  { "data": {
                      "form": form,
                  }})