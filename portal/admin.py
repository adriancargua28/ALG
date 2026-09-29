from django.contrib import admin

from .models import AreaEstudio, HitoAcademico, PerfilProfesional, Principio

admin.site.site_header = "Panel de administración · Adriana Lara Gutiérrez"
admin.site.site_title = "Administración del portal"
admin.site.index_title = "Gestión de contenidos"


@admin.register(PerfilProfesional)
class PerfilProfesionalAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "numero_colegiada", "actualizado")
    readonly_fields = ("actualizado",)
    fieldsets = (
        ("Identidad", {"fields": ("nombre_completo", "titular", "presentacion")}),
        (
            "Datos profesionales",
            {"fields": ("situacion", "numero_colegiada", "colegio_profesional", "idiomas")},
        ),
        (
            "Contacto",
            {"fields": ("ciudad", "email", "telefono", "linkedin_url")},
        ),
        ("Franjas visuales", {"fields": ("lema_juzgado", "lema_internacional")}),
        ("Aviso legal", {"fields": ("aviso_legal", "actualizado")}),
    )

    def has_add_permission(self, request):
        # Perfil único: solo se permite crearlo si todavía no existe.
        return not PerfilProfesional.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AreaEstudio)
class AreaEstudioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ambito", "orden", "publicada")
    list_editable = ("orden", "publicada")
    list_filter = ("ambito", "publicada")
    search_fields = ("titulo", "resumen", "descripcion")
    prepopulated_fields = {"slug": ("titulo",)}


@admin.register(HitoAcademico)
class HitoAcademicoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "institucion", "periodo", "orden", "publicado")
    list_editable = ("orden", "publicado")
    list_filter = ("categoria", "publicado")
    search_fields = ("titulo", "institucion", "descripcion")


@admin.register(Principio)
class PrincipioAdmin(admin.ModelAdmin):
    list_display = ("titulo", "orden", "publicado")
    list_editable = ("orden", "publicado")
    search_fields = ("titulo", "texto")
