
from django.urls import path
from . import views

urlpatterns = [    

    path('chat', views.chat, name = 'chat'),          

    #path('home', views.home, name = 'home'),

    

               
    #path('start2', views.start2, name = 'start2'),
    #path('interfon2/<str:location>/<str:name>/', views.interfon2, name = 'interfon2'),                  
               
                                    
               
    # path('start', views.start, name = 'start'),   
    # path('interfon/<str:location>/<str:name>/', views.interfon, name = 'interfon'),
    
    
    

    # path("testws/", views.testws, name="testws"),
    
    # #path("", views.index, name="index"),
    # path("<str:room_name>/", views.room, name="room"),
    
    
]
