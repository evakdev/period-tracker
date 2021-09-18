from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views import View
from django.http import request
from .forms import SignUpForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

MyUser = get_user_model()


@csrf_exempt
def SignUpPage(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("User Created!")
        else:
            isbound = form.is_bound
            er = form.errors
            return HttpResponse(isbound, er)

    if request.method == "GET":
        return render(request, "signup.html", context={"SignUpForm": SignUpForm()})


def SignInPage(request):
    if request.method == "GET":
        return HttpResponse("Please login first!")


@login_required(login_url="/users/signin")
def profilePage(request):
    user = request.user
    info = {"id": user.unique_id, "email": user.email, "birthday": user.date_of_birth}
    pfp_url = user.picture

    return render(request, "profile.html", context={"info": info, "pfp_url": pfp_url})
