from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'

# def authenticate(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         # user = aut
#         # print(user)
#
#     form = AuthenticationForm()
#     return render(request, 'login.html',
#               {"data": {
#                   "form": form,
#               }})