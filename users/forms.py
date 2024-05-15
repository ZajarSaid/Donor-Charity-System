from django import forms
from .models import  CustomUser,Charithy
from Activity.models import Venue, Event, Post, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


INPUT_CLASSES = 'form-control'


class LoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

        widgets = {
            'email':forms.TextInput(attrs={'class':INPUT_CLASSES}),
            'password':forms.PasswordInput(attrs={'class':INPUT_CLASSES}),
        }



class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = CustomUser
		fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'status','password1', 'password2')

        


       
        


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'status', 'password','image')

        widgets={
                
             'username':forms.TextInput(attrs={'class':INPUT_CLASSES}),
             'first_name':forms.TextInput(attrs={'class':INPUT_CLASSES}),
             'last_name':forms.TextInput(attrs={'class':INPUT_CLASSES}),
             'email':forms.EmailInput(attrs={'class':INPUT_CLASSES}),
             'phone':forms.TextInput(attrs={'class':INPUT_CLASSES}),
             'status':forms.Select(attrs={'class':INPUT_CLASSES}),
             'image':forms.FileInput(attrs={'class':INPUT_CLASSES}),
             'password':forms.PasswordInput(attrs={'class':INPUT_CLASSES}),
             
            }




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
                'event_date':forms.DateInput(attrs={'class':INPUT_CLASSES}),
                
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

