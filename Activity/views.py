from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from Activity.models import Event
from users.models import Charithy, CustomUser
import os
from django.conf import settings
from users.forms import AddVenueForm, AddEventForm, AddPostForm, CommentForm, UserForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Donation
from django.urls import reverse
from django.contrib.auth import logout

# Create your views here
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from users.models import Charithy

import pandas as pd
import plotly.express as px
import plotly.io as pio


def charity_age_trends(request):
    
    charithies = Charithy.objects.all()
    
    # Convert the data to a pandas DataFrame
    data = {
        'First Name': [charity.first_name for charity in charithies],
        'Age': [charity.age for charity in charithies]
    }
    df = pd.DataFrame(data)
    
    # Create a bar graph using Plotly
    fig = px.histogram(df, x='Age', nbins=10, title='Trends of Charities by Age')
    # fig.update_traces(marker_color='blue')  # Update the color of the bars to green
    fig.update_layout(
        xaxis_title='Age',
        yaxis_title='Number of Charities',
        bargap=0.2,
        title={'x': 0.5}  # Center the title
    )
    
    # Convert the plotly figure to HTML
    graph_html = pio.to_html(fig, full_html=False)
    
    # Render the template with the graph
    return render(request, 'Activity/Charity_Trends.html', {'graph': graph_html})

def generate_pdf_report(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="charities_report.pdf"'

    # Create the PDF object
    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    elements = []

    # Add titles
    styles = getSampleStyleSheet()
    custom_title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        alignment=1,  # Center alignment
    )

    ministry_title = Paragraph("Ministry of Social Welfare", custom_title_style)
    elements.append(ministry_title)
    elements.append(Spacer(1, 12))  # Add a space after the ministry title

    charity_title = Paragraph("THE LIST OF CHARITY", styles['Title'])
    elements.append(charity_title)
    elements.append(Spacer(1, 12))  # Add a space after the charity title

    # Fetch data from the database
    charithies = Charithy.objects.all()

    # Create table data
    data = [['Image', 'First Name',  'Last Name', 'Sex', 'Age', 'Needs', 'Created At']]
    for charithy in charithies:
        # Handling the image
        if charithy.image:
            image_path = os.path.join(settings.MEDIA_ROOT, charithy.image.name)
            img = Image(image_path, 1*inch, 1*inch)  # Resize the image to fit the table cell
        else:
            img = "No Image"

        needs_list = [Paragraph(need.name, styles['BodyText']) for need in charithy.needs.all()]  # Assuming Needs has a 'name' field
        needs_paragraph = Paragraph('<br/>'.join([n.text for n in needs_list]), styles['BodyText'])
        data.append([img, charithy.first_name, charithy.last_name, charithy.get_sex_display(),
         charithy.age, needs_paragraph, charithy.created_at.strftime('%Y-%m-%d %H:%M:%S')])

    # Create the table
    table = Table(data)

    # Add style
    style = TableStyle([
         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (4, -1), 'CENTER'),  # Center align first five columns
        ('ALIGN', (6, 1), (6, -1), 'CENTER'),  # Center align the 'Created At' column
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment to middle
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    return response


def export_pdf(request):
    template_path = 'report/charity.html'
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
        form = AddEventForm(request.POST, request.FILES)
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

