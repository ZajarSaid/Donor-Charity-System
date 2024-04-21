from django.urls import path
from . import views


app_name = 'User'

urlpatterns = [
    path('index',views.index, name='index'),
    path('', views.home, name='home'),
    path('profile/<username>',views.Profile, name='user-profile'),
    path('Add-charity', views.Add_charity, name='add-charity')
]
