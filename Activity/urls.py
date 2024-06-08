from django.urls import path
from . import views

app_name = 'Activity'

urlpatterns = [
    path('', views.index, name='index'),
    path('Add-venue/',views.add_venue, name='add-venue'),
    path('Add-event/',views.add_event, name='add-event'),
    path('Add-post/',views.add_post, name='add-post'),
    path('Add-user/',views.add_user, name='add-user'),
    path('post/<int:pk>',views.post, name='post'),
    path('Allposts',views.list_post, name='postss'),
    path('posts/',views.posts, name='posts'),
    # path('Add-comment/<int:post_id>',views.add_comment, name='add-comment'),
    path('Events/',views.list_events, name='events'),
    path('event/<int:pk>',views.event, name='event'),
    path('update-event/<int:pk>',views.update_event, name='update-event'),
    path('update-post/<int:pk>',views.edit_post, name='update-post'),
    path('delete-event/<int:event_id>', views.delete_event, name='delete-event'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete-post'),
    path('charity/', views.all_charity, name='all-charity'),
    path('users/', views.all_users, name='all-users'),
    path('donation/', views.all_donations, name='donations'),
    path('Approve-Event/<int:pk>', views.approve_event, name='event-approve'),
    path('Deny-Event/<int:event_pk>', views.deny_event, name='event-denial'),
    path('logout/', views.user_logout, name='logout'),
    path('ExportPDF/', views.export_pdf, name='export-pdf')



]
