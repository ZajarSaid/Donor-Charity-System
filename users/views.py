from django.shortcuts import render
from django.http import HttpResponse


from .forms import CharityForm
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.




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
    
    return HttpResponse("wooooooooooooooooooooooooo.")