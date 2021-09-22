from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import SignInForm, SignUpForm


class SignInPage(LoginView):
    form_class = SignInForm
    template_name = 'signin.html'
    redirect_authenticated_user = True

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


@login_required(login_url="/users/signin")
def profilePage(request):
    user = request.user
    info = {"id": user.unique_id, "email": user.email, "birthday": user.date_of_birth}
    pfp_url = user.picture

    return render(request, "profile.html", context={"info": info, "pfp_url": pfp_url})
