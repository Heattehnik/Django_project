from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect
from django.conf import settings
import random
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm
from users.models import User


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:catalog')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        send_mail(
            f'Регистрация прошла успешно',
            f'Вы зарегистрировались на платформе!',
            settings.EMAIL_HOST_USER,
            [self.object.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    send_mail(
        f'Новый пароль',
        f'Ваш новый пароль {new_password}',
        settings.EMAIL_HOST_USER,
        [request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:catalog'))
