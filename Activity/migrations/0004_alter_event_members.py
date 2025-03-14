# Generated by Django 5.0.3 on 2024-04-27 13:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0003_alter_event_event_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='events_attending', to=settings.AUTH_USER_MODEL),
        ),
    ]
