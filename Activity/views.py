from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from Activity.models import Event
from users.models import Charithy, CustomUser

from users.forms import AddVenueForm, AddEventForm, AddPostForm, CommentForm, UserForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Donation
from django.urls import reverse
from django.contrib.auth import logout

# Create your views here

from django.template.loader import get_template
from xhtml2pdf import pisa

def export_pdf(request):
    template_path = 'Activity/charity.html'
    charity = Charithy.objects.all()
    context = {
        'myvar':'heeeeeeeeeeeeeeeeey',
        'charity':charity
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename=ListOfChariy.pdf' 
   
    
    #find a template and render it
    template = get_template(template_path)
    html = template.render(context)

    #create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    #if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some bla  bla blaaaaaaaa <prev>' + html +'</prev>')
    return response

def add_user(request):
    title = 'Add-User'
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserForm(request.POST or None, request.FILES)
            if form.is_valid():
                password = form.cleaned_data['password'] 
                user = form.save(commit=False)
                user.set_password(password)
                user.email = form.cleaned_data['email']
                user.save()
                messages.success(request, 'a user has been added sussceesfully..')
            else:
                messages.success(request, 'a user has not been added sussceesfully..')
                
                return redirect('Activity:all-users')
    form = UserForm()

    return render(request, 'Activity/Add_user.html', {'form':form, 'title':title})

def all_donations(request):
    donations = Donation.objects.values()

    return render(request, 'tests/donation.html', {'donations':donations})


def all_users(request):
    users = CustomUser.objects.values()

    return render(request, 'tests/users.html', {'users':users})

def all_charity(request):
    charity = Charithy.objects.all()
    title = 'All Charity'

    context={
        'charity':charity,
        'title':title
    }

    return render(request, 'tests/charity.html', context)



def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    messages.error(request, "the event has beeen successfuly deleted")

    return redirect('Activity:events')


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    
    messages.error(request, "the post has beeen successfuly deleted")

    return redirect('Activity:posts')


#individual post
def post(request, pk):
    c_post = get_object_or_404(Post, pk=pk)
    # event.delete()

    return render(request, 'Activity/post.html',{'u_post':c_post})


def edit_post(request, pk):
    if request.user.is_authenticated:

        u_post = Post.objects.get(pk=pk)
        title = 'Update-Post'

        if request.method == 'POST':
            form = AddPostForm(request.POST or None, instance=u_post)
            if form.is_valid():
                form.save()
                messages.success(request, "the event has been updated successfuly..!")
            
                return redirect('Activity:post', pk=u_post.id)

        form = AddPostForm(instance=u_post)
    else:
        messages.success(request, "you have to be logged in first ..")
        return redirect('Activity:add-post')
    
        

    return render(request, 'Activity/update_post.html',{ 'form':form,'title':title})



def approve_event(request, pk):
    p_event = get_object_or_404(Event, pk=pk)

    p_event.approved = True
    p_event.save()
    messages.success(request, "your event has been approved successfully")
        
    return redirect('Activity:event', pk=p_event.id)


def deny_event(request, event_pk):
    p_event = get_object_or_404(Event, pk=event_pk)

    if p_event.approved == True:
        p_event.approved = False
        p_event.save()

    
    
        messages.info(request, "your event has been denied successfully")
        
    return redirect('Activity:event', pk=p_event.id)


#list of events to the page wih minimal implementatkon
def _events(request):
    all_events = Event.objects.all()

    title = 'All events'

    return render(request, 'Activity/_events.html', {'title':title, 'Events':all_events})


def update_event(request, pk):
    if request.user.is_authenticated:

        u_event = Event.objects.get(pk=pk)
        title = 'Update-Event'

        if request.method == 'POST':
            form = AddEventForm(request.POST or None, instance=u_event)
            if form.is_valid():
                form.save()
                messages.info(request, "event updated successfuly..!")
            
                return redirect('Activity:event', pk=u_event.id)

        form = AddEventForm(instance=u_event)
    else:
        messages.error(request, "you have to be logged in first ..")
        return redirect('Activity:add-event')
    
        

    return render(request, 'Activity/update_event.html',{ 'form':form,'title':title})

def event(request, pk):
    c_event = get_object_or_404(Event, pk=pk)
    # event.delete()
    # messages.success(request, "the event has beeen successfuly deleted")
    return render(request, 'Activity/event.html',{'c_event':c_event})


# list events on the admin table
def list_events(request):
    all_events = Event.objects.all()

    title = 'All events'

    return render(request, 'Activity/events.html', {'title':title, 'Events':all_events})


def index(request):

    return render(request, 'website/index.html')

def list_post(request):
    title = 'Posts'
    
    List_posts = Post.objects.all()
    
    return render(request, 'website/about.html', {'Posts':List_posts})

# list of posts to user
def posts(request):
    title = 'Posts'
    
    List_posts = Post.objects.select_related('author').all()
    
    return render(request, 'Activity/posts.html', {'All_posts':List_posts})

def add_comment(request, post_id):
    #retrieve a post
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('Website:post')
        
        messages.success(request, 'your commennt has been added successfully')
    form = CommentForm()
    return redirect('Website:post')


def add_post(request):
    created = False
    title = 'Create a Post'
    
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect('/Activity/Add-post?created')
        
    if 'created' in request.GET:
        created = True
        messages.success(request, 'your Post has been created successfully')
    form = AddPostForm()
    return render(request, 'Activity/Add_post.html',{'form':form, 'title':title})

def add_venue(request):
    submitted = False
    title = 'Add-Venue'
    
    if request.method == 'POST':
        form = AddVenueForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Activity/Add-venue?submitted')
        
    if 'submitted' in request.POST:
        submitted = True
        messages.success(request, 'your form has been created successfully')
    form = AddVenueForm()
    return render(request, 'Activity/Add_venue.html',{'form':form, 'title':title})



def add_event(request):
    submitted = False
    title = 'Add-Event'
    
    if request.method == 'POST':
        form = AddEventForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/Activity/Add-event?submitted')
        
    if 'submitted' in request.GET:
        submitted = True
        messages.success(request, 'your Event has been created successfully')
    form = AddEventForm()
    return render(request, 'Activity/Add_event.html',{'form':form, 'title':title})

def user_logout(request):
    logout(request)
    messages.error(request, 'you have been logged out successfuly')
    return HttpResponseRedirect(reverse('Website:index'))

