from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from. forms import LoginForm


class UserLoginView(LoginView):

    template_name = "accounts/login.html"

    authentication_form = LoginForm

    redirect_authenticated_user = True

    def form_valid(self, form):

        messages.success(
            self.request,
            f"Welcome back, {form.get_user().username}!",
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            "Invalid username or password.",
        )

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy(
            "dashboard:redirect"
        )


class UserLogoutView(LogoutView):

    next_page = reverse_lazy(
        "accounts:login"
    )