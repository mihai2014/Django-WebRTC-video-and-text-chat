from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.http import HttpResponse

# @login_required
def home(request):
    #return HttpResponse(f"<h1>Welcome {request.user.username}</h1>")
    return render(request, 'home.html', {})

