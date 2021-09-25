from django.urls import path

from .views import (
    PasswordResetCompletePage,
    PasswordResetConfirmPage,
    PasswordResetDonePage,
    LoginPage,
    LogoutPage,
    ProfilePage,
    PasswordChangePage,
    PasswordChangeDonePage,
    PasswordResetPage,
    RegisterPage,
)

urlpatterns = [
    path("register", RegisterPage.as_view(), name="register"),
    path("profile", ProfilePage.as_view(), name="profile"),
    path("login", LoginPage.as_view(), name="login"),
    path("logout", LogoutPage.as_view(), name="logout"),
    path("password_change/", PasswordChangePage.as_view(), name="password_change"),
    path("password_change/done/",PasswordChangeDonePage.as_view(),name="password_change_done"),
    path("password_reset/", PasswordResetPage.as_view(), name="password_reset"),
    path("password_reset/done/", PasswordResetDonePage.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/",PasswordResetConfirmPage.as_view(),name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompletePage.as_view(), name="password_reset_complete"),
]
