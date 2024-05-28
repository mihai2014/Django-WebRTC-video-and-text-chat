"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('chat/', include('chat.urls')),
    path('', include('accounts.urls')),
    path('', include('chat.urls')),
] + static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, 'static'))   # for developing with daphne

# /home/mihai/venv2/lib/python3.10/site-packages/django/contrib/admin/static/

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print(settings.STATIC_ROOT)
print(os.path.join(BASE_DIR, 'static'))