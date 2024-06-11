import random

from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import CustomUser, Charithy


class command(BaseCommand):
    help = 'create charity data'

    def handle(self, *args, **kwargs):

        # get or create superuser

        # user = CustomUser.objects.filter(username='admin')
        # if not user.exists():
        #     user = CustomUser.objects.create_superuser(username='admin', password='test123')
        # else:
        #     user = user.first()

        #    first_name, middle_name, last_name, image, sex, age, created_at

        charity = []
                  




        ]


