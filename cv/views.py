from django.shortcuts import render
from .models import Perfil, Educacion, Experiencia, Habilidad, Referencia

def home(request):
    return render(request, 'cv/home.html')

def cv_view(request):
    perfil = Perfil.objects.first()
    educacion = Educacion.objects.all()
    experiencia = Experiencia.objects.all()
    habilidades = Habilidad.objects.all()
    referencias = Referencia.objects.all()

    context = {
        'perfil': perfil,
        'educacion': educacion,
        'experiencia': experiencia,
        'habilidades': habilidades,
        'certificados': perfil.certificados.all() if perfil else [],
        'proyectos': perfil.proyectos.all() if perfil else [],
        'referencias': referencias,
        'garage': perfil.garage.filter(activarparaqueseveaenfront=True) if perfil else [],
    }

    return render(request, 'cv/cv.html', context)
