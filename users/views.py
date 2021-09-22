from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from .forms import SignInForm, SignUpForm


class SignInPage(LoginView):
    form_class = SignInForm
    template_name = "signin.html"
    redirect_authenticated_user = True


class SignUpPage(View):
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            login(request,user)
            return redirect("/users/profile")
        else:
            isbound = form.is_bound
            er = form.errors
            return HttpResponse(isbound, er)

    def get(self, request):
        return render(request, "signup.html", context={"SignUpForm": SignUpForm()})


@method_decorator(login_required(login_url="/users/signin"), name="dispatch")
class ProfilePage(View):
    def get(self, request):
        user = request.user
        info = {
            "id": user.unique_id,
            "email": user.email,
            "birthday": user.date_of_birth,
        }
        pfp_url = user.picture

        return render(
            request, "profile.html", context={"info": info, "pfp_url": pfp_url}
        )
