# Generated by Django 5.0.3 on 2024-04-26 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charithy',
            name='age',
            field=models.PositiveIntegerField(),
        ),
    ]
