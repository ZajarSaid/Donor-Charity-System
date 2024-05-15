from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser
from Activity.models import Post, Event, Donation

from .forms import CharityForm, UserForm
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.


def Add_charity(request):
    title = 'Add-charity'
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CharityForm(request.POST or None, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'A charity member has been added successfuly')
                return redirect('Activity:all-charity')
    form = CharityForm()
    return render(request, 'Activity/Add_charity.html', {'form':form, 'title':title})


def Profile(request, username):
    user = CustomUser.objects.get(username=username)
    if request.method == 'POST':
        form = UserForm(request.POST or None,instance = user)
        if form.is_valid():
            form.save()
            messages.success(request, 'your profile has been updated successfulyy')
            return redirect('users')
    title = 'Profile'
    form = UserForm(request.POST or None,instance = user)
    return render(request, 'Activity/user_profile.html', {'form':form, 'title':title})


def index(request):
    submitted = False
    if request.method == 'POST':
        form = CharityForm(request.POST or None)
        if form.is_valid():
            user=form.save(commit=False)
            user.created_by = request.user
            user.save()
            return HttpResponseRedirect('index?submitted')
    if submitted in request.GET:
        submitted = True
        messages.success(request, 'your form has been created successfully')
    form = CharityForm
    return render(request, 'tests/register_charity.html', {'form':form})



def home(request):
    events = Event.objects.all()
    posts = Post.objects.all()
    users = CustomUser.objects.all()
    donations = Donation.objects.all()

    context={
        'events':events,
        'donations':donations,
        'posts':posts,
        'users':users
    }
    
    return render(request, 'Activity/dashboard.html', context)

