# Generated by Django 5.0.3 on 2024-04-26 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(verbose_name='Date'),
        ),
    ]
