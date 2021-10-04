from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm

class LoginPage(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True


class RegisterPage(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            return redirect("/users/profile")
        else:
            isbound = form.is_bound
            er = form.errors
            return HttpResponse(isbound, er)

    def get(self, request):
        return render(request, "users/register.html", context={"form": RegisterForm()})


@method_decorator(login_required(login_url="/users/login"), name="dispatch")
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
            request, "users/profile.html", context={"info": info, "pfp_url": pfp_url}
        )


class LogoutPage(LogoutView):
    template_name = 'users/logged_out.html'

class PasswordChangePage(PasswordChangeView):
    template_name = 'users/password_change_form.html'

class PasswordChangeDonePage(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

class PasswordResetPage(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'

class PasswordResetDonePage(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class PasswordResetConfirmPage(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'

class PasswordResetCompletePage(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'