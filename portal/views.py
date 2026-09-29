from django.shortcuts import render
from django.views.decorators.http import require_safe

from .models import AreaEstudio, HitoAcademico, PerfilProfesional, Principio

# El sitio público no ejecuta scripts: la política de seguridad de contenido
# lo impone también a nivel de navegador (script-src queda cubierto por
# default-src 'none').
POLITICA_CSP = "; ".join(
    [
        "default-src 'none'",
        "style-src 'self'",
        "img-src 'self' data:",
        "base-uri 'none'",
        "form-action 'none'",
        "frame-ancestors 'none'",
    ]
)


@require_safe
def index(request):
    perfil = PerfilProfesional.load()

    areas = list(AreaEstudio.objects.filter(publicada=True))
    claves_presentes = {area.ambito for area in areas}
    ambitos = [
        (clave, etiqueta)
        for clave, etiqueta in AreaEstudio.Ambito.choices
        if clave in claves_presentes
    ]

    hitos = list(HitoAcademico.objects.filter(publicado=True))
    grupos = []
    for clave, etiqueta in HitoAcademico.Categoria.choices:
        items = [hito for hito in hitos if hito.categoria == clave]
        if items:
            grupos.append({"clave": clave, "etiqueta": etiqueta, "items": items})

    principios = list(Principio.objects.filter(publicado=True))

    respuesta = render(
        request,
        "portal/index.html",
        {
            "perfil": perfil,
            "areas": areas,
            "ambitos": ambitos,
            "grupos": grupos,
            "principios": principios,
        },
    )
    respuesta["Content-Security-Policy"] = POLITICA_CSP
    return respuesta
