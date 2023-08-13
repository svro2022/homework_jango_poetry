from django.urls import path
from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, ConfirmPage


app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/confirm_email/', ConfirmPage.as_view(), name='confirm_email'),
]
