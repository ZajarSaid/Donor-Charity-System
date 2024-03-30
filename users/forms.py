from django import forms
from .models import  CustomUser,Charithy
from Activity.models import Venue, Event, Post, Comment


INPUT_CLASSES = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        
        widgets={
                
                'body':forms.Textarea(attrs={'class':INPUT_CLASSES}),
            }

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body','photo')
        
        widgets={
                'title':forms.TextInput(attrs={'class':INPUT_CLASSES}),
                'body':forms.Textarea(attrs={'class':INPUT_CLASSES}),
                
                'photo':forms.FileInput(attrs={'class':INPUT_CLASSES}),
            }

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'description')
            
        widgets={
                'name':forms.TextInput(attrs={'class':INPUT_CLASSES}),
                'venue':forms.Select(attrs={'class':INPUT_CLASSES}),
                
                'manager':forms.Select(attrs={'class':INPUT_CLASSES}),
                'description':forms.Textarea(attrs={'class':INPUT_CLASSES}),
                
            }

class AddVenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'phone')
            
        widgets={
                'name':forms.TextInput(attrs={'class':INPUT_CLASSES}),
                'address':forms.TextInput(attrs={'class':INPUT_CLASSES}),
                'phone':forms.TextInput(attrs={'class':INPUT_CLASSES}),
                
            }


class CharityForm(forms.ModelForm):
    class Meta:
        model = Charithy
        fields = ('first_name', 'middle_name', 'last_name','image', 'sex', 'age')
        
        widgets={
            'first_name':forms.TextInput(attrs={'class':INPUT_CLASSES}),
            'middle_name':forms.TextInput(attrs={'class':INPUT_CLASSES}),
            'last_name':forms.TextInput(attrs={'class':INPUT_CLASSES}),
            'image':forms.FileInput(attrs={'class':INPUT_CLASSES}),
            
            
        }

