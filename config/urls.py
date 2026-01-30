"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cv.urls')),
]

from django.http import HttpResponse
from django.contrib.auth import get_user_model

def crear_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='JeanS').exists():
        User.objects.create_superuser('JeanS', 'florespilosojeanpierre@gmail.com', 'Jampi21.')
        return HttpResponse('Usuario JeanS creado exitosamente')
    return HttpResponse('Usuario JeanS ya existe')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear-admin-temp/', crear_admin),
    path('', include('cv.urls')),
]