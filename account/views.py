from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from account.forms import LoginForm, RegistrationForm


class LoginView(View):
    """
    View to log in.

    To log in, user should provide e-mail address and password.
    The default Django authentication has been adjusted to accept e-mail rather than username (see authentication.py).
    """
    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    url_next = request.GET.get("next", "/")
                    return redirect(url_next)
                else:
                    form.add_error("email", "Account is blocked.")
            else:
                form.add_error("email", "Incorrect email or password.")
        return render(request, "account/login.html", {"form": form})


class RegisterView(View):
    """
    View to register.

    The app uses e-mail address to authenticate so username is a consecutive number.
    """
    def get(self, request):
        form = RegistrationForm()
        return render(request, "account/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            new_user.username = new_user.id
            new_user.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
        return render(request, "account/register.html", {"form": form})
