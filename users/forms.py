from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from catalog.forms import StyleFormMixin
from django import forms


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    '''Регистрация пользователя'''

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    '''Профиль пользователя'''

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'avatar', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        '''Скрыть пароль в профиле'''
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
