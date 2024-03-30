from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.



from django.shortcuts import render, get_object_or_404, redirect
from users.forms import AddVenueForm, AddEventForm, AddPostForm, CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post
# Create your views here.


def index(request):
    return HttpResponse("hey")

def posts(request):
    title = 'Posts'
    
    List_posts = Post.objects.select_related('author').all()
    
    return render(request, 'Activity/posts.html', {'All_posts':List_posts})

def add_comment(request, pk):
    title = 'Comment'
    #retrieve a post
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('/add-comment')
        
        messages.success(request, 'your commennt has been added successfully')
    form = CommentForm()
    return render(request, 'Activity/comment.html',{'form':form, 'title':title})


def add_post(request):
    created = False
    title = 'Create a Post'
    
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect('Add-post/?created')
        
    if created in request.POST:
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
            return HttpResponseRedirect('Activity/Add-venue/?submitted')
        
    if submitted in request.POST:
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
            return HttpResponseRedirect('Activity/Add-event/?submitted')
        
    if submitted in request.POST:
        submitted = True
        messages.success(request, 'your form has been created successfully')
    form = AddEventForm()
    return render(request, 'Activity/Add_event.html',{'form':form, 'title':title})

