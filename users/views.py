from base64 import b64encode

from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.shortcuts import render, redirect, HttpResponse

from .forms import CustomAuthForm, CustomUserCreationForm, CustomPasswordChangeForm, UserProfileForm
from .models import User, UserAvatar

from core.storage import AvatarFileStorage, AvatarFileRetrieval


# Create your views here.
class CustomLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = 'users/templates/login.html'
    extra_context = {
        "data": {
            "next": "/"
        }
    }


class CustomLogoutView(LogoutView):
    template_name = 'users/templates/logout.html'


def register_new_user_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            return redirect("/users/registration_successful")

    else:
        form = CustomUserCreationForm()

    return render(request, 'users/templates/register.html',
                  {"data": {
                          "form": form,
                  }})


def registration_successful_view(request):
    return render(request, 'users/templates/registration_successful.html')


def user_profile_view(request):
    user = User.objects.get(id=request.user.id)
    form = UserProfileForm({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }, {})
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['avatar'] is not None:
                image = AvatarFileStorage(file=form.cleaned_data['avatar'], user=user)
                image.update()
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()

    avatar = AvatarFileRetrieval(user)
    avatar_instance = ""
    avatar_bytes = ""
    try:
        avatar_instance = avatar.getavatarinstance()
    except UserAvatar.DoesNotExist as e:
        print("An error occurred: {0} - inspect user_profile_view.".format(e.__str__()))
    else:
        avatar_bytes = str(avatar.getb64encodedimage())[2:-1]  # Removes [b']......[']

    return render(request, "users/templates/user_profile.html",
                  { "data": {
                      "user": user,
                      "form": form,
                      "avatar": avatar_instance,
                      "avatar_bytes": avatar_bytes,
                  }})


class ChangePasswordView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users/templates/change_password.html"
    extra_context = {}
    # return render(request, "users/templates/change_password.html")


def about_the_author_view(request):
    return render(request, "users/templates/author.html")


def get_avatar(request):
    user = User.objects.get(id=request.user.id)
    avatar = AvatarFileRetrieval(user).get()
    avatar_bytes = str(b64encode(avatar.avatar.tobytes()))[2:-1]
    return HttpResponse("data:image/png;base64," + avatar_bytes)
