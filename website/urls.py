from django.urls import path
from . import views
from .views import RegistrationView, UsernameValidationView, EmailValidationView, Post_Comment_View
from django.views.decorators.csrf import csrf_exempt

app_name = 'Website'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('register/', RegistrationView.as_view(), name='register'),
    path('Profile/<email>', views.User_profile, name='profile'), 
    path('Postz/', views.Post_Comment_View.as_view(), name='post'),
    path('About/', views.about, name='about'),
    path('Events/', views._events, name='events'),
    path('JoinEvent/<int:event_pk>/<username>', views.join_event, name='join-event'),
    path('LeaveEvent/<int:event_pk>/<username>', views.leave_event, name='leave-event')
]
