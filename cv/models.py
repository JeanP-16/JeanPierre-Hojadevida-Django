from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
from django.core.files.base import ContentFile
from pdf2image import convert_from_path
import requests
import io
import os


# ============================================
# FUNCIONES DE VALIDACIÓN (REGLAS DEL INGENIERO)
# ============================================

def validate_cedula_ecuador(value):
    """Valida que la cédula tenga exactamente 10 dígitos numéricos"""
    if not value.isdigit():
        raise ValidationError('La cédula debe contener solo números.')
    if len(value) != 10:
        raise ValidationError('La cédula debe tener exactamente 10 dígitos.')

def validate_birth_year(value):
    """Valida nacimiento entre 1980 y la actualidad"""
    year = value.year
    current_year = date.today().year
    if year < 1980 or year > current_year:
        raise ValidationError(f'El año de nacimiento debe estar entre 1980 y {current_year}.')

def validate_certificate_year(value):
    """Valida certificados/reconocimientos entre 2007 y la actualidad"""
    year = value.year
    current_year = date.today().year
    if year < 2007 or year > current_year:
        raise ValidationError(f'La fecha debe estar entre el año 2007 y {current_year}.')

# ============================================
# MODELO: Perfil
# ============================================
class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    profesion = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    # VALIDACIÓN DE CÉDULA (10 DÍGITOS)
    cedula = models.CharField(
        max_length=10, 
        unique=True,
        validators=[validate_cedula_ecuador],
        verbose_name="Cédula",
        help_text="Debe tener 10 dígitos exactos."
    )
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)
    lugar_nacimiento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Lugar de Nacimiento")
    
    # VALIDACIÓN DE FECHA NACIMIENTO (1980-Actualidad)
    fecha_nacimiento = models.DateField(
        validators=[validate_birth_year],
        verbose_name="Fecha de Nacimiento",
        help_text="Año permitido: 1980 en adelante."
    )
    sexo = models.CharField(max_length=20, blank=True, null=True)
    
    estado_civil = models.CharField(max_length=20, blank=True, null=True, verbose_name="Estado Civil")
    licencia = models.CharField(max_length=20, blank=True, null=True, help_text="Ej: Tipo B")
    telefono = models.CharField(max_length=20, verbose_name="Teléfonos")
    
    domicilio = models.CharField(max_length=200, blank=True, null=True, verbose_name="Domicilio")
    trabajo = models.CharField(max_length=200, blank=True, null=True, verbose_name="Trabajo")
    
    email = models.EmailField()
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicación General (Ciudad/País)")
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    
    foto = models.ImageField(upload_to='perfil/', blank=True, null=True, help_text='Foto de perfil')

    class Meta:
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return self.nombre

# ============================================
# MODELO: Educación
# ============================================
class Educacion(models.Model):
    institucion = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    fecha_inicio = models.DateField(validators=[validate_certificate_year])
    fecha_fin = models.DateField(blank=True, null=True, validators=[validate_certificate_year])
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_inicio'] # Orden Cronológico
        verbose_name_plural = "Educación"

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"

# ============================================
# MODELO: Experiencia Laboral
# ============================================
class Experiencia(models.Model):
    empresa = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    fecha_inicio = models.DateField(validators=[validate_certificate_year])
    fecha_fin = models.DateField(blank=True, null=True, validators=[validate_certificate_year])
    descripcion = models.TextField()

    class Meta:
        ordering = ['-fecha_inicio'] # Orden Cronológico
        verbose_name_plural = "Experiencias"

    def __str__(self):
        return f"{self.cargo} en {self.empresa}"

# ============================================
# MODELO: Habilidad
# ============================================
class Habilidad(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name_plural = "Habilidades"
        ordering = ['-nivel', 'nombre']

    def __str__(self):
        return f"{self.nombre} (Nivel {self.nivel}/5)"

# ============================================
# MODELO: Certificado (CURSOS)
# ============================================
class Certificado(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="certificados")
    titulo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200)
    
    # VALIDACIÓN FECHA (2007-Actualidad)
    fecha = models.DateField(
        validators=[validate_certificate_year],
        help_text="Fecha de emisión (2007 en adelante)"
    )
    
    archivo = models.FileField(upload_to="certificados/", blank=True, null=True)

    imagen = models.ImageField(
    upload_to="certificados/img/",
    blank=True,
    null=True,
    help_text="Imagen generada automáticamente desde el PDF"
    )

    class Meta:
        ordering = ['-fecha'] # Orden Cronológico
        verbose_name_plural = "Certificados"

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"


# ============================================
# MODELO: Reconocimiento (NUEVO)
# ============================================
class Reconocimiento(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="reconocimientos")
    titulo = models.CharField(max_length=200, verbose_name="Título del Reconocimiento")
    otorgado_por = models.CharField(max_length=200, verbose_name="Entidad que otorga")
    
    # VALIDACIÓN FECHA (2007-Actualidad)
    fecha = models.DateField(
        validators=[validate_certificate_year],
        help_text="Fecha de obtención (2007 en adelante)"
    )
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to="reconocimientos/", blank=True, null=True)

    class Meta:
        ordering = ['-fecha'] # Orden Cronológico
        verbose_name_plural = "Reconocimientos"

    def __str__(self):
        return self.titulo

# ============================================
# MODELO: Proyecto
# ============================================
class Proyecto(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="proyectos")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tecnologias = models.CharField(max_length=300)
    github = models.URLField(blank=True, null=True)
    demo = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.nombre

# ============================================
# MODELO: Referencia
# ============================================
class Referencia(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Referencias"

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"

# ============================================
# MODELO: Garage
# ============================================
class Garage(models.Model):
    ESTADO_CHOICES = [('Bueno', 'Bueno'), ('Regular', 'Regular')]
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="garage")
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40, choices=ESTADO_CHOICES)
    descripcion = models.TextField()
    valordelbien = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    imagen = models.ImageField(upload_to="garage/", blank=True, null=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Producto de Garage"
        verbose_name_plural = "Productos de Garage"

    def __str__(self):
        return f"{self.nombreproducto} - ${self.valordelbien}"