from django.contrib.auth.forms import UserCreationForm
from users.models import User
from catalog.forms import StyleFormMixin


class UserForm(StyleFormMixin, UserCreationForm):
    '''Регистрация пользователя'''

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
