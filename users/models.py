from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator as FeV

# Create your models here.

EX_FILE_VALIDATOR = FeV(['csv'])
EX_IMAGE_VALIDATOR = FeV(['jpg','jpeg', 'png'])

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        # Your custom user creation logic
        if not email:
            raise ValueError("users must have an email")
        if not username:
            raise ValueError("users must have a username")
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractUser):
    STATUS = (
        ('regular', 'regular'),
        ('government', 'government'),
        ('donor','donor')
    )
    first_name = models.CharField(max_length=123, null=True)
    last_name = models.CharField(max_length=123,  null=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=123,unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=200, default='+255')
    status = models.CharField(max_length=200, choices=STATUS, default='regular')
    image = models.ImageField(null=True, blank=True, upload_to='Profiles/', validators=[EX_IMAGE_VALIDATOR])
    password = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # Provide unique related_name for groups
    
    
    def __str__(self):
        return self.username
    
    def get_username(self):
        return self.username
    
    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    

    
class Charithy(models.Model):
    
    SEX = (
        ('male', 'M'),
        ('female', 'F'),
        
    )
    
    first_name = models.CharField(max_length=123)
    middle_name = models.CharField(max_length=123)
    last_name = models.CharField(max_length=123)
    image = models.ImageField(null=True, blank=True, upload_to='Profiles/', validators=[EX_IMAGE_VALIDATOR])
    sex = models.CharField(max_length=200, choices=SEX, default='male')
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    #registered_by = models.ForeignKey(CustomUser, related_name='charity', on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name_plural = 'Charithies'
        ordering = ('age',)
    
    def __str__(self):
        return self.first_name
    
    


