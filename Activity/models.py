from django.db import models

from users.models import CustomUser

class Venue(models.Model):
    name = models.CharField('Name', max_length=128)
    address = models.CharField('Address', max_length=128)
    phone = models.CharField('Phone', max_length=128)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField('Name', max_length=128)
    event_date = models.DateTimeField('Date')
    venue = models.ForeignKey(Venue, related_name='events', blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(CustomUser, related_name='managed_events', null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='Events/', blank=True)
    members = models.ManyToManyField(CustomUser, related_name='events_attending', blank=True)
    approved = models.BooleanField(default=False)

    def is_user_joined(self, user_id):
        return self.members.filter(pk=user_id).exists()
    
    def __str__(self):
        return self.name

class Donation(models.Model):
    amount = models.FloatField()
    donated_at = models.DateTimeField(auto_now_add=True)
    donor = models.ForeignKey(CustomUser, related_name='donations_given', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Donation {self.pk}"
    
    
class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='Posts/')
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)  # Changed related_name

    def __str__(self):
        return self.body