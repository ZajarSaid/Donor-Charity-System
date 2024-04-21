from django.shortcuts import render, redirect
from users.forms import SignUpForm, UserForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import CustomUser

from Activity.models import Event

from django.views import View
from django.http import JsonResponse
import json
from validate_email import validate_email



# Create your views here.
class RegistrationView(View):
    def get(self, request):

        return render(request, 'website/register.html')

    def post(self, request):
        #GET USER DATA
        #VALIDATE
        #Create a user Account

        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        context = {'FieldValues':request.POST}

        if not CustomUser.objects.filter(username=username).exists():
            if not CustomUser.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'your password is too short')

                    return render(request, 'website/register.html', context)

                #the default avlue of status is donor here
                user = CustomUser.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, phone=phone)
                user.set_password(password)
                user.save()
                messages.success(request, 'A user account has been created successfuly..')

                render(request, 'website/register.html')

        render(request, 'website/register.html')


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric character'})
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username is already taken, choose another'})
        return JsonResponse({'username_valid':True})
    
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'email is invalid'}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'this email is already taken, choose another'})
        return JsonResponse({'email_valid':True})



def user_login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
      
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            messages.success(request, 'you have been logged in successfuly..')
            return redirect('User:home')
        # if CustomUser.objects.filter(password=password).exists():
            
            print(password)
                
    form = LoginForm()
    return render(request, 'website/weblogin.html', {'form':form})


def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None)
    
    events = Event.objects.filter(approved=False)

    form = UserForm()
    return render(request, 'demo/temp.html', {'form':form, 'Events':events})

