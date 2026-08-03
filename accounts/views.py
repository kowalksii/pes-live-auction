from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, RegistrationForm
from .models import User
from .services.registration import register_participant


class UserLoginView(LoginView):

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):

        response = super().form_valid(form)

        user = form.get_user()
        user.is_online = True
        user.save(update_fields=["is_online"])

        messages.success(
            self.request,
            f"Welcome back, {user.username}!",
        )

        return response

    def form_invalid(self, form):

        messages.error(
            self.request,
            "Invalid username or password.",
        )

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy("dashboard:redirect")


class UserLogoutView(LogoutView):

    next_page = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            request.user.is_online = False
            request.user.save(update_fields=["is_online"])

        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):

    model = User
    form_class = RegistrationForm
    template_name = "accounts/register.html"

    success_url = reverse_lazy("accounts:registration_success")

    def form_valid(self, form):

        self.object = register_participant(form)

        return redirect("accounts:registration_success")


class RegistrationSuccessView(TemplateView):

    template_name = "accounts/registration_success.html"


class PendingApprovalView(TemplateView):

    template_name = "accounts/pending_approval.html"