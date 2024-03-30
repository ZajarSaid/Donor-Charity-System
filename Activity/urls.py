from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('Add-venue/',views.add_venue, name='add-venue'),
    path('Add-event/',views.add_event, name='add-event'),
    path('Add-post/',views.add_post, name='add-post'),
    path('posts/',views.posts, name='posts'),
    path('Add-comment/<int:pk>',views.add_comment, name='add-comment')


]
