from django.shortcuts import render, redirect, get_object_or_404
from users.forms import SignUpForm, UserForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import CustomUser
from django.urls import reverse
from django.http import HttpResponseRedirect

from Activity.models import Event, Post, Comment

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
import json
from validate_email import validate_email



# Create your views here.

def leave_event(request, event_pk, username):

    user = get_object_or_404(CustomUser, username = username)
    event = get_object_or_404(Event, pk = event_pk)

    if event:
        event.members.remove(user)
        messages.success(request, 'you have been successfuly removed from the event members ')

        return HttpResponseRedirect(reverse('Website:events') + '?left')

    
    return render(request, 'website/events.html')


def join_event(request, event_pk, username):

    user = get_object_or_404(CustomUser, username = username)
    event = get_object_or_404(Event, pk = event_pk)

    if event:
        event.members.add(user)
        messages.success(request, 'you have been successfuly joined the event')

        return HttpResponseRedirect(reverse('Website:events') + '?joined')

    
    return render(request, 'website/events.html')



def about(request):
  
    return render(request, 'website/about.html')


class Post_Comment_View(LoginRequiredMixin, View):
    template_name = 'website/NewPost.html'


    def get(self, request, *arg, **kwargs):
        all_posts = Post.objects.all()

        return render(request, self.template_name, {'Posts':all_posts})

    def post(self, request, *arg, **kwargs):

        comment = request.POST['comment_text']
        author = request.user
        post_id = request.POST['post_id']

        if comment and post_id:
            post = get_object_or_404(Post, id=post_id)

        post_comment = Comment.objects.create(
            body=comment, 
            post=post,
            author=author
            )

        post_comment.save()

        print(post_comment.post.title)
        print(post_comment.post.author)
        print(post_comment.author)
        
        messages.success(request, 'your comment has been added successfully')
       
        return redirect('Website:post')


def post(request):
    all_posts = Post.objects.all()


    return render(request, 'website/NewPost.html', {'Posts':all_posts})


def _events(request):
    all_events = Event.objects.all()

    title = 'All events'

    return render(request, 'website/events.html', {'title':title, 'Events':all_events})

def User_profile(request, email):
    user = get_object_or_404(CustomUser, email=email)

    return render(request, 'website/Profile.html', {'User':user})



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

                # the default value of status is donor here
                user = CustomUser.objects.create_user(
                 username=username,
                 first_name=firstname,
                 last_name=lastname,
                 email=email, phone=phone
                 )
                user.set_password(password)
                user.save()
                messages.success(request, 'A user account has been created successfuly..')
                return redirect('Website:register')

                return render(request, 'Website/register.html')

        return render(request, 'website/register.html')


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
        
            
            print(password)
                
    form = LoginForm()
    return render(request, 'website/weblogin.html', {'form':form})


def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None)
    
    events = Event.objects.all()

    form = UserForm()
    return render(request, 'website/base.html', {'form':form, 'Events':events})

