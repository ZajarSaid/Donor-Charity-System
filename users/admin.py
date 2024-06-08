from django.contrib import admin
from .models import CustomUser, Charithy, Needs
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Charithy)
admin.site.register(Needs)