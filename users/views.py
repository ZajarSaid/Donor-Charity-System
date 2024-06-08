from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import CustomUser, Needs
from Activity.models import Post, Event, Donation
from .models import Charithy
from .forms import CharityForm, UserForm
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseBadRequest
from django.contrib import messages
# Create your views here.


def Add_charity(request):
    title = 'Add-charity'
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.POST)
            first_name = request.POST['first_name']
            middle_name = request.POST['middle_name']
            last_name = request.POST['last_name']
            sex = request.POST['sex']
            age = request.POST['age']
            image = request.FILES.get('image')
            needs_ids = request.POST.getlist('needs')

            if not needs_ids:
                return HttpResponseBadRequest('Needs are required')

            # needs = get_object_or_404(Needs, pk=needs_ids)

            charity = Charithy.objects.create(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                sex=sex,
                age=age,
                image=image,
            )
            charity.needs.set(needs_ids)  # Set the ManyToMany relationship
            charity.save()
            messages.success(request, 'A charity member has been added successfuly')
            return redirect('Activity:all-charity')
        else:

            print(request.POST)
    needs = Needs.objects.all()
    form = CharityForm()
    context={
        'title':title,
        'needs':needs,
        'form':form,
    }
    return render(request, 'Activity/Add_charity.html', context)


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

