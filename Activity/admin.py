from django.contrib import admin
from .models import Venue, Post, Event, Donation, Comment
# Register your models here.



admin.site.register(Venue)
admin.site.register(Post)
admin.site.register(Donation)
admin.site.register(Event)
admin.site.register(Comment)