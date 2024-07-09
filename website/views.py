from django.shortcuts import render, redirect, get_object_or_404
from users.forms import SignUpForm, UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from Activity.models import Event, Post, Comment, Donation

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
import json
from validate_email import validate_email
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
from django.utils import timezone



class PaymentView(LoginRequiredMixin, View):
    template_name = 'website/payment.html'

    def get(self, request):

        return render(request, self.template_name)

    def post(self, request):

        user_pk = request.user.id
        amount = request.POST['amount']

        donor = CustomUser.objects.filter(pk=user_pk)
        if donor:
            Donation.objects.create(amount=amount, donor=donor)
            messages.success(request, 'You have been successfuly donated to our organization..')
            return redirect('Website:payment')
        else:
            messages.error(request, 'there are an error fetching your ur credentials..')
            return redirect('Website:payment')

        


def payments(request):
    
    return render(request, 'website/payment.html')


class NewConversationView(View):
    Status = 'regular'
    template_name = 'website/newConversation.html'

    def get(self, request):
        user_pk = request.user.pk
        conversation = Conversation.objects.filter(members__in=[request.user.id])
    
        if conversation:
            return redirect('Website:messages', c_id=conversation.first().id)
        
        form = ConversationMessageForm()
        context={
            'form':form,  
        }

        return render(request, self.template_name, context)

    def post(self, request):

        form = ConversationMessageForm(request.POST)
        # take admin as an initial member of conversation
        admin = CustomUser.objects.filter(status=self.Status).first()
        print(admin)

        if form.is_valid():
            conversation = Conversation.objects.create(created_at=timezone.now())
            conversation.members.add(admin)
            conversation.members.add(request.user)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            messages.success(request, 'Your Message has been sent successfuly')

            
            # for message in Conversation.messages.all():
            #     if message.created_by == request.user.id:
            #         m_id = message.pk
            # m_id = message.pk
            return redirect('Website:inbox')

        context={
            'form':form
        }

        return render(request, self.template_name, context)


@login_required

def messages_view(request, c_id):
    # take conversation/user_id
    u_id = request.user.id
    conversation = Conversation.objects.filter(members__in=[u_id]).get(pk=c_id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation_message=form.save(commit=False)
            conversation_message.created_by = request.user
            conversation_message.conversation = conversation
            conversation_message.save()
            
            conversation.save()
            # messages.success(request, 'your message has been sent successfuly..')
            
            return redirect('Website:messages', c_id=c_id)
            
            
    form = ConversationMessageForm()

    context={
        'form':form,
        'conversation':conversation
    }

    return render(request, 'website/messages.html', context)




class Conversation_Inbox_View(View):
    pass

class DonationView(View):
    template_name = 'website/account_donation.html'

    def get(self, request):
        return render(request, self.template_name)

class EventsView(View):
    template_name = 'website/donor_events.html'

    def get(self,request):
        donor_id = request.user.pk 
        joined_events = Event.objects.filter(members__in=[donor_id])

        context={
            'Events':joined_events
        }
        return render(request, self.template_name, context)

class InboxView(View):
    template_name = 'website/inbox.html'
    

    def get(self, request):
        user_pk = request.user.pk
        user_conversations = Conversation.objects.filter(members__in=[user_pk])

        form = ConversationMessageForm()

        context={
            'form':form,
            'user_conversations':user_conversations
        }

        return render(request, self.template_name, context)


class DonorrProfileView(View):

    template_name = 'Website/user_profile.html'

    def get(self, request):
        user_pk = request.user.pk
        userInfo = get_object_or_404(CustomUser, pk=user_pk)

        if userInfo.status == 'regular':
            return redirect('User:home')

        form = UserForm(instance=userInfo)
        user = userInfo
        context = {
            'form':form,
            'user':user
            }    

        return render(request,self.template_name , context)

    def post(self, request):
        user_pk = request.user.pk
        userInfo = get_object_or_404(CustomUser, pk=user_pk)
        form = UserForm(request.POST, request.FILES, instance=userInfo)

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        image = request.FILES.get('image')
        phone = request.POST['phone']
    
        c_user = CustomUser.objects.get(id=user_pk)
        c_user.username = username
        c_user.last_name = last_name
        c_user.first_name = first_name
        c_user.email = email
        c_user.image = image
        c_user.phone = phone
        c_user.save()
        messages.success(request, 'Your information has been updated successfuly..')

        return redirect('Website:user-page')



def User_profile_page(request):

    user_pk = request.user.pk
    userInfo = get_object_or_404(CustomUser, pk=user_pk)

    if userInfo.status == 'regular':
        return redirect('User:home')

    

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=userInfo)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        image = request.FILES.get('image')
        phone = request.POST['phone']
    
        c_user = CustomUser.objects.get(id=user_pk)
        c_user.username = username
        c_user.last_name = last_name
        c_user.first_name = first_name
        c_user.email = email
        c_user.image = image
        c_user.phone = phone
        c_user.save()
        messages.success(request, 'Your information has been updated successfuly..')
        return redirect('Website:user-page')

    form = UserForm(instance=userInfo)
    user = userInfo
    context = {
        'form':form,
        'user':userInfo
    }
    
    return render(request, 'Website/user_profile.html', context)

def leave_event(request, event_pk, username):

    user = get_object_or_404(CustomUser, username = username)
    event = get_object_or_404(Event, pk = event_pk)

    if event:
        event.members.remove(user)
        messages.error(request, 'you have been successfuly removed from the event members ')

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
        image = request.FILES.get('image')
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
                 email=email,
                 phone=phone,
                 image=image
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
            if user.status == 'donor':
                login(request, user)
                messages.success(request, 'you have been logged in successfuly..')
                return redirect('Website:user-page')
                
            login(request, user)
            messages.success(request, 'you have been logged in successfuly..')
            return redirect('User:home')
        
        messages.error(request, 'there is an erro loggin in.')
        return redirect('Website:login')

       
                
    form = LoginForm()
    return render(request, 'website/Login.html', {'form':form})

def user_logout(request):
    if request.user is not None:
        logout(request)
        
        return redirect('Website:index')


def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None)
    
    events = Event.objects.all()

    form = UserForm()
    return render(request, 'website/base1.html', {'form':form, 'Events':events})

