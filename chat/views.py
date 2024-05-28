from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect


def chat(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, "chat0.html",{"user_name":username})
    else:
        return HttpResponseRedirect('/')




def home(request):
    return HttpResponse("<h1>Hello!</h1>")
    #return render(request, 'home.html', {})
    #return render(request, "chat/test_webrtc.html")



# def start2(request):
#     print("index")
#     return render(request, "chat/connect_user2.html")

# def interfon2(request,location,name):
#     return render(request, "chat/interfon_nou.html",{"room_name": location,"name":name})



# def start(request):
#     print("index")
#     return render(request, "chat/connect_user.html")

# def interfon(request,location,name):
#     return render(request, "chat/interfon.html",{"room_name": location,"name":name})



# def index(request):
#     print("index")
#     return render(request, "chat/index.html")


# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})