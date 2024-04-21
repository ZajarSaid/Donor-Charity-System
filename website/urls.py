from django.urls import path
from . import views
from .views import RegistrationView, UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt

app_name = 'Website'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('register/', RegistrationView.as_view(), name='register')
]
