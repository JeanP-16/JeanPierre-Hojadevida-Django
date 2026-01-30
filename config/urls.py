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
from django.http import HttpResponse
from django.contrib.auth import get_user_model

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cv.urls')),
]


def crear_admin(request):
    User = get_user_model()
    # CAMBIA ESTOS DATOS por los que TÚ creaste
    User.objects.create_superuser('JeanPierre', 'florespilosojeanpierre@gmail.com', 'Jean21.')
    return HttpResponse('Usuario admin creado')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear-admin-temporal/', crear_admin),  # ESTA LÍNEA
    # tus otras rutas...
]