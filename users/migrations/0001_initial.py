# Generated by Django 5.0.3 on 2024-03-29 08:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=123, null=True)),
                ('last_name', models.CharField(max_length=123, null=True)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('email', models.EmailField(max_length=123, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(default='+255', max_length=200)),
                ('status', models.CharField(choices=[('regular', 'regular'), ('government', 'government'), ('donor', 'donor')], default='regular', max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='User_profile/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('password', models.CharField(max_length=120, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
