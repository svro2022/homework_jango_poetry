from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy, reverse
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm
from config import settings
from django.core.mail import send_mail
from users.email_services import sendmail
from django.shortcuts import redirect
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class LoginView(BaseLoginView):
    '''Контроллер входа в профиль пользователя'''
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    '''Контроллер выхода из профиля пользователя'''
    pass


class RegisterView(CreateView):
    '''Контроллер регистрации пользователя'''
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # '''Отправка письма на email'''
        # new_user = form.save()
        # send_mail(
        # subject='Поздравляем с регистрацией',
        # message='Вы зарегистрировались на нашей платформе',
        # from_email=settings.EMAIL_HOST_USER,
        # recipient_list=[new_user.email]
        # )

        '''Отправка письма-подтверждения на email'''

        if form.is_valid:
            new_user = form.save()
            sendmail(
                f'Для подтверждения почты пройдите по ссылке http://127.0.0.1:8000/{new_user.pk}/confirm_email/',
                (new_user.email,),
            )
        return super().form_valid(form)


class ConfirmPage(TemplateView):
    '''Подтверждение почты'''
    template_name = 'users/confirm_email.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        pk = context_data['pk']
        if User.objects.filter(pk=pk).exists():
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.is_staff = True
            user.save()
        return context_data


class UserUpdateView(LoginRequiredMixin, UpdateView):
    '''Профиль пользователя'''
    '''LoginRequiredMixin - скрывают контент от неавторизованных пользователей'''
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def generate_new_password(request):
    '''Изменение пароля'''
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:index'))
