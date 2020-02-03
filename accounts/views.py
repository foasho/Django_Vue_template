from django.shortcuts import render
from django.views import generic

from django.contrib.auth import get_user_model
from .forms import (
    LoginForm,
)

from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,TemplateView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.shortcuts import redirect, resolve_url

class IndexView(generic.TemplateView):
    template_name = "index.html"

class SignIn(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'login/signin.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('register:console', pk=self.request.user.pk)

class SignUp(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'login/signin.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('register:console', pk=self.request.user.pk)