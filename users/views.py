from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from users.models import User
from users.forms import UserForm
from config import settings
from django.core.mail import send_mail
from users.email_services import sendmail


class LoginView(BaseLoginView):
    '''Контроллер входа в профиль пользователя'''
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    '''Контроллер выхода из профиля пользователя'''
    pass


class RegisterView(CreateView):
    '''Контроллер регистрации пользователя'''
    model = User
    form_class = UserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        '''Отправка письма на email'''

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
                f'Для верификации почты пройдите по ссылке http://127.0.0.1:8000/users/confirm_email/{new_user.pk}',
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


