from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.files.base import ContentFile
import requests
import tempfile
import os
import io
from pdf2image import convert_from_path
from .models import Habilidad

from .models import (
    Perfil, Educacion, Experiencia, Habilidad,
    Certificado, Proyecto, Reconocimiento, Referencia, Garage
)

# ============================================
# ADMIN: Perfil
# ============================================
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesion', 'email', 'tiene_foto')
    search_fields = ('nombre', 'email')
    
    fieldsets = (
        ('👤 Información Principal', {
            'fields': (
                'nombre', 'profesion', 'descripcion', 'foto'
            )
        }),
        ('🆔 Identificación', {
            'fields': (
                'cedula', 'nacionalidad', 
                'fecha_nacimiento', 'lugar_nacimiento',
                'sexo'
            )
        }),
        ('📞 Contacto (Estado, Licencia, Tel)', {
            'fields': (
                'estado_civil', 'licencia', 'telefono',
                'email', 'ubicacion'
            )
        }),
        ('🏠 Domicilio', {
            'fields': ('domicilio',)
        }),
        ('🏢 Trabajo', {
            'fields': ('trabajo',)
        }),
        ('🌐 Redes Sociales', {
            'fields': ('linkedin', 'github')
        }),
    )
    
    def tiene_foto(self, obj):
        if obj.foto:
            return mark_safe('<span style="color: green;">✅ Sí</span>')
        return mark_safe('<span style="color: red;">❌ No</span>')
    
    tiene_foto.short_description = 'Foto'


# ============================================
# ADMIN: Educación
# ============================================
@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'fecha_inicio', 'fecha_fin', 'estado')
    search_fields = ('titulo', 'institucion')
    list_filter = ('fecha_inicio', 'fecha_fin')
    date_hierarchy = 'fecha_inicio'
    
    def estado(self, obj):
        if obj.fecha_fin:
            return mark_safe('<span style="color: gray;">✓ Completado</span>')
        return mark_safe('<span style="color: blue;">⏱ En curso</span>')
    
    estado.short_description = 'Estado'


# ============================================
# ADMIN: Experiencia
# ============================================
@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'fecha_inicio', 'fecha_fin', 'estado')
    search_fields = ('cargo', 'empresa')
    list_filter = ('fecha_inicio', 'fecha_fin')
    date_hierarchy = 'fecha_inicio'
    
    def estado(self, obj):
        if obj.fecha_fin:
            return mark_safe('<span style="color: gray;">✓ Completado</span>')
        return mark_safe('<span style="color: green;">⏱ Actual</span>')
    
    estado.short_description = 'Estado'


# ============================================
# ADMIN: Habilidad
# ============================================
@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'nivel', 'perfil', 'orden')
    list_filter = ('categoria', 'perfil')
    search_fields = ('nombre', 'categoria')
    list_editable = ('orden', 'nivel')
    ordering = ('orden', 'categoria', 'nombre')
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('perfil', 'categoria', 'nombre')
        }),
        ('Nivel de Dominio', {
            'fields': ('nivel',),
            'description': 'Indica tu nivel de dominio en porcentaje (0-100%)'
        }),
        ('Orden de Aparición', {
            'fields': ('orden',),
            'description': 'Número más bajo aparece primero'
        }),
    )


# ============================================
# ADMIN: Certificado
# ============================================
@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'institucion', 'fecha', 'perfil', 'preview_archivo')
    search_fields = ('titulo', 'institucion')
    list_filter = ('fecha', 'perfil')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('📜 Información del Certificado', {
            'fields': ('perfil', 'titulo', 'institucion')
        }),
        ('📅 Fecha', {
            'fields': ('fecha',)
        }),
        ('📎 Archivo', {
            'fields': ('archivo',),
            'description': '⚠️ IMPORTANTE: El archivo se guarda en Azure: media/certificados/'
        }),
    )
    
    def preview_archivo(self, obj):
        if obj.archivo:
            try:
                nombre = obj.archivo.name.lower()
                if nombre.endswith('.pdf'):
                    return format_html(
                        '<a href="{}" target="_blank" style="color: #dc3545; text-decoration: none;">'
                        '<span style="font-size: 1.3em;">📄</span> PDF</a>',
                        obj.archivo.url
                    )
                else:
                    return format_html(
                        '<a href="{}" target="_blank">'
                        '<img src="{}" style="max-width: 100px; max-height: 50px; border-radius: 5px;"/></a>',
                        obj.archivo.url, obj.archivo.url
                    )
            except Exception:
                pass
        return mark_safe('<span style="color: gray;">❌ Sin archivo</span>')
    
    preview_archivo.short_description = 'Vista Previa'

    readonly_fields = ("preview_imagen",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if (
            obj.archivo
            and obj.archivo.name.lower().endswith(".pdf")
            and not obj.imagen
        ):
            self._generar_imagen_desde_pdf(obj)

    def _generar_imagen_desde_pdf(self, obj):
        # 1️⃣ Descargar PDF desde Azure
        response = requests.get(obj.archivo.url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        try:
            # 2️⃣ Convertir PDF → imagen
            pages = convert_from_path(
                tmp_path,
                dpi=200,
                first_page=1,
                last_page=1
            )

            buffer = io.BytesIO()
            pages[0].save(buffer, format="JPEG", quality=90)
            buffer.seek(0)

            nombre = os.path.splitext(
                os.path.basename(obj.archivo.name)
            )[0]

            # 3️⃣ Guardar imagen en Azure
            obj.imagen.save(
                f"{nombre}.jpg",
                ContentFile(buffer.read()),
                save=False
            )

            obj.save(update_fields=["imagen"])

        finally:
            os.remove(tmp_path)

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-width:120px;border-radius:8px;" />',
                obj.imagen.url
            )
        return "—"


# ============================================
# ADMIN: Proyecto
# ============================================
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'perfil', 'tiene_github', 'tiene_demo')
    search_fields = ('nombre', 'descripcion', 'tecnologias')
    list_filter = ('perfil',)
    
    def tiene_github(self, obj):
        if obj.github:
            return format_html('<a href="{}" target="_blank">🔗 GitHub</a>', obj.github)
        return '—'
    
    tiene_github.short_description = 'GitHub'
    
    def tiene_demo(self, obj):
        if obj.demo:
            return format_html('<a href="{}" target="_blank">🔗 Demo</a>', obj.demo)
        return '—'
    
    tiene_demo.short_description = 'Demo'


# ============================================
# ADMIN: Referencia
# ============================================
@admin.register(Referencia)
class ReferenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'empresa', 'telefono', 'email')
    search_fields = ('nombre', 'empresa', 'cargo')
    list_filter = ('empresa',)

# ============================================
# ADMIN: Reconocimiento
# ============================================
@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'otorgado_por', 'fecha', 'perfil')
    search_fields = ('titulo', 'otorgado_por')
    list_filter = ('fecha',)

# ============================================
# ADMIN: Garage
# ============================================
@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'perfil', 'activarparaqueseveaenfront', 'preview_imagen')
    search_fields = ('nombreproducto', 'descripcion')
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront', 'perfil')
    
    fieldsets = (
        ('📦 Información del Producto', {
            'fields': ('perfil', 'nombreproducto', 'descripcion')
        }),
        ('📸 Imagen del Producto', {
            'fields': ('imagen',),
            'description': '⚠️ IMPORTANTE: La imagen se guarda en Azure: media/garage/'
        }),
        ('💰 Detalles de Venta', {
            'fields': ('estadoproducto', 'valordelbien', 'activarparaqueseveaenfront')
        }),
    )
    
    def preview_imagen(self, obj):
        if obj.imagen:
            try:
                return format_html(
                    '<a href="{}" target="_blank">'
                    '<img src="{}" style="max-width: 100px; max-height: 50px; border-radius: 5px;"/></a>',
                    obj.imagen.url, obj.imagen.url
                )
            except Exception:
                pass
        return mark_safe('<span style="color: gray;">❌ Sin imagen</span>')
    
    preview_imagen.short_description = 'Vista Previa'


admin.site.site_header = '🎓 Sistema CV - Panel de Administración'
admin.site.site_title = 'CV Admin'
admin.site.index_title = 'Gestión de Hoja de Vida Profesional'

