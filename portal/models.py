"""Modelos del portal profesional de Adriana Lara Gutiérrez."""
from django.db import models

MARCADOR_COLEGIADA = "[Nº Colegiada pendiente de colegiación / Editable]"

PRESENTACION_POR_DEFECTO = (
    "Análisis jurídico con visión internacional. Mi enfoque combina rigor "
    "técnico, claridad expositiva y respeto a los principios deontológicos de "
    "la profesión, en asuntos donde confluyen el ordenamiento nacional, el "
    "europeo y el internacional."
)

LEMA_JUZGADO_POR_DEFECTO = "El rigor jurídico se construye con fuentes, método y criterio."
LEMA_INTERNACIONAL_POR_DEFECTO = (
    "Un mismo asunto, varios ordenamientos: todo análisis empieza por saber cuál se aplica."
)

AVISO_LEGAL_POR_DEFECTO = (
    "La información publicada en este sitio tiene carácter exclusivamente "
    "informativo y académico. No constituye asesoramiento jurídico ni establece "
    "relación profesional alguna entre abogado y cliente.\n\n"
    "El contenido describe un perfil académico. Los datos de colegiación se "
    "publicarán únicamente cuando exista la correspondiente inscripción en el "
    "colegio profesional, y las titulaciones se indicarán solo una vez "
    "acreditadas."
)


def es_marcador(texto):
    """Indica si un texto es un marcador provisional del tipo «[... / Editable]»."""
    texto = (texto or "").strip()
    return texto.startswith("[") and texto.endswith("]")


class PerfilProfesional(models.Model):
    """Ficha única (singleton) con los datos públicos de la titular del sitio."""

    nombre_completo = models.CharField(
        "nombre completo", max_length=120, default="Adriana Lara Gutiérrez"
    )
    titular = models.CharField(
        "titular",
        max_length=160,
        default="Perfil Académico en Derecho y Relaciones Internacionales",
        help_text=(
            "Fórmula de presentación. No atribuir titulaciones definitivas "
            "que no estén acreditadas."
        ),
    )
    presentacion = models.TextField(
        "presentación",
        default=PRESENTACION_POR_DEFECTO,
        help_text="Separa los párrafos con una línea en blanco.",
    )
    situacion = models.CharField(
        "situación actual",
        max_length=60,
        blank=True,
        default="Próxima graduación",
        help_text="Texto del sello de la ficha. Déjalo vacío para ocultarlo.",
    )
    numero_colegiada = models.CharField(
        "número de colegiada",
        max_length=80,
        default=MARCADOR_COLEGIADA,
        help_text=(
            "Mientras no exista colegiación, mantén el marcador entre corchetes. "
            "Sustitúyelo por el número real cuando proceda."
        ),
    )
    colegio_profesional = models.CharField(
        "colegio profesional", max_length=160, blank=True
    )
    idiomas = models.CharField("idiomas de trabajo", max_length=160, blank=True)
    ciudad = models.CharField("ubicación", max_length=120, blank=True)
    email = models.EmailField("correo electrónico", blank=True)
    telefono = models.CharField("teléfono", max_length=30, blank=True)
    linkedin_url = models.URLField("perfil profesional (URL)", blank=True)
    lema_juzgado = models.CharField(
        "lema (franja del juzgado)", max_length=200, default=LEMA_JUZGADO_POR_DEFECTO
    )
    lema_internacional = models.CharField(
        "lema (franja internacional)",
        max_length=200,
        default=LEMA_INTERNACIONAL_POR_DEFECTO,
    )
    aviso_legal = models.TextField(
        "aviso legal y deontológico", default=AVISO_LEGAL_POR_DEFECTO
    )
    actualizado = models.DateTimeField("última modificación", auto_now=True)

    class Meta:
        verbose_name = "perfil profesional"
        verbose_name_plural = "perfil profesional"

    def __str__(self):
        return self.nombre_completo

    def save(self, *args, **kwargs):
        # Modelo singleton: solo puede existir el registro con pk=1.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Devuelve el perfil guardado o uno con valores por defecto sin guardar."""
        return cls.objects.filter(pk=1).first() or cls()

    @property
    def colegiada_pendiente(self):
        return es_marcador(self.numero_colegiada)

    @property
    def tiene_contacto(self):
        return bool(self.email or self.telefono or self.linkedin_url or self.ciudad)


class AreaEstudio(models.Model):
    """Área de estudio e interés mostrada en el acordeón filtrable."""

    class Ambito(models.TextChoices):
        DERECHO = "derecho", "Derecho"
        INTERNACIONAL = "internacional", "Ámbito internacional"
        TRANSVERSAL = "transversal", "Enfoque transversal"

    ambito = models.CharField(
        "ámbito", max_length=20, choices=Ambito.choices, default=Ambito.DERECHO
    )
    titulo = models.CharField("título", max_length=140)
    slug = models.SlugField("identificador", max_length=160, unique=True)
    resumen = models.CharField("resumen", max_length=240)
    descripcion = models.TextField(
        "descripción",
        blank=True,
        help_text="Separa los párrafos con una línea en blanco.",
    )
    orden = models.PositiveSmallIntegerField("orden", default=0)
    publicada = models.BooleanField("publicada", default=True)

    class Meta:
        ordering = ("orden", "titulo")
        verbose_name = "área de interés profesional"
        verbose_name_plural = "áreas de interés profesional"

    def __str__(self):
        return self.titulo


class HitoAcademico(models.Model):
    """Entrada de la sección «Formación y trayectoria»."""

    class Categoria(models.TextChoices):
        FORMACION = "formacion", "Formación académica"
        TRAYECTORIA = "trayectoria", "Trayectoria profesional"
        INVESTIGACION = "investigacion", "Investigación y publicaciones"

    categoria = models.CharField(
        "categoría",
        max_length=20,
        choices=Categoria.choices,
        default=Categoria.FORMACION,
    )
    titulo = models.CharField("título", max_length=160)
    institucion = models.CharField("institución", max_length=160, blank=True)
    periodo = models.CharField("periodo", max_length=80, blank=True)
    descripcion = models.TextField("descripción", blank=True)
    orden = models.PositiveSmallIntegerField("orden", default=0)
    publicado = models.BooleanField("publicado", default=True)

    class Meta:
        ordering = ("orden", "id")
        verbose_name = "hito de formación o trayectoria"
        verbose_name_plural = "hitos de formación y trayectoria"

    def __str__(self):
        return self.titulo

    @property
    def institucion_provisional(self):
        return es_marcador(self.institucion)

    @property
    def periodo_provisional(self):
        return es_marcador(self.periodo)

    @property
    def descripcion_provisional(self):
        return es_marcador(self.descripcion)


class Principio(models.Model):
    """Criterio de trabajo mostrado en la sección «Enfoque»."""

    titulo = models.CharField("título", max_length=100)
    texto = models.TextField("texto")
    orden = models.PositiveSmallIntegerField("orden", default=0)
    publicado = models.BooleanField("publicado", default=True)

    class Meta:
        ordering = ("orden", "id")
        verbose_name = "criterio de trabajo"
        verbose_name_plural = "criterios de trabajo"

    def __str__(self):
        return self.titulo
