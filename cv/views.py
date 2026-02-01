from django.shortcuts import render
from .models import Perfil, Educacion, Experiencia, Certificado, Reconocimiento, Proyecto, Garage, Habilidad  # ← AGREGAR Proyecto y Habilidad

from .models import Habilidad


def home(request):
    return render(request, 'cv/home.html')

def cv_view(request):
    perfil = Perfil.objects.first()
    educacion = Educacion.objects.filter(perfil=perfil).order_by('-fecha_inicio')
    experiencia = Experiencia.objects.filter(perfil=perfil).order_by('-fecha_inicio')
    habilidades = Habilidad.objects.filter(perfil=perfil)
    certificados = perfil.certificados.all().order_by('-fecha')
    proyectos = Proyecto.objects.filter(perfil=perfil)
    garage = Garage.objects.filter(perfil=perfil)
    
    context = {
        'perfil': perfil,
        'educacion': educacion,
        'experiencia': experiencia,
        'habilidades': habilidades,
        'certificados': certificados,
        'proyectos': proyectos,
        'garage': garage,
    }
    
    return render(request, 'cv/cv.html', context)