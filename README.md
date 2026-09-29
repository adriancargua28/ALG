# Adriana Lara Gutiérrez · Portal profesional

Sitio web profesional de **Adriana Lara Gutiérrez** (Derecho y Relaciones Internacionales).
Proyecto Django 4.2 (LTS) con una sola página pública, gestión de contenidos desde el panel de administración y **cero JavaScript** en el sitio público.

## Principios del proyecto

- **Sin JavaScript.** No hay ficheros de script, etiquetas de script ni manejadores de eventos en línea. La navegación usa anclas; el filtrado por ámbito, radios con `:checked`; los acordeones, `<details>/<summary>`; los estados, `:hover` y `:focus-visible`. Además, la respuesta de la portada incluye una cabecera `Content-Security-Policy` que prohíbe cualquier script a nivel de navegador.
- **Deontología.** La ficha profesional mantiene la fórmula «Perfil Académico en Derecho y Relaciones Internacionales». No se atribuyen titulaciones que no estén acreditadas. El número de colegiada muestra el marcador `[Nº Colegiada pendiente de colegiación / Editable]` hasta que exista colegiación real.
- **Compatibilidad.** Python 3.9 a 3.12; Linux, macOS y Windows.

## Diseño y movimiento

Tema oscuro con acentos en oro y azul, y tres ilustraciones vectoriales propias en `static/img/` (`juzgado.svg`, `mundo.svg`, `favicon.svg`).

| Efecto | Cómo se hace, sin JavaScript |
|---|---|
| Barra de progreso lateral, cabecera que se compacta, portada que se desvanece al bajar | `animation-timeline: scroll(root)` |
| Aparición de bloques, parallax de las franjas de imagen, línea de la cronología que se dibuja | `animation-timeline: view()` |
| Frases que se escriben en la portada | `@keyframes` con `steps()` |
| Sello de la ficha, globo giratorio, marquesina de áreas | `@keyframes` por tiempo |

Los efectos ligados al scroll están dentro de `@supports (animation-timeline: view())`. Funcionan en Chrome y Edge 115+ y en Safari 26+. En navegadores sin soporte (Firefox, mientras siga tras un flag) la página se ve completa, sin esos efectos. Con `prefers-reduced-motion` se desactivan todas las animaciones.

### Sustituir las ilustraciones por fotografías

Guarda la foto en `static/img/` (por ejemplo `juzgado.jpg`) y cambia la ruta `url()` en `static/css/styles.css`:

- `.banda--juzgado .banda__fondo` (franja del juzgado) y `.hero__juzgado` (portada).
- `.banda--mundo .banda__fondo` (franja internacional) y `.hero__mundo` (portada).

Mantén los degradados que acompañan a la imagen: garantizan que el texto siga siendo legible. Usa fotos de tu propiedad o con licencia que permita su uso comercial, y comprímelas (por debajo de unos 300 KB).

> El panel de administración (`/admin/`) es el de Django y usa sus propios recursos internos. No forma parte del sitio público ni del código de este repositorio.

## Estructura

```
.
├── manage.py
├── requirements.txt
├── core/                 # Configuración del proyecto (settings, urls, wsgi, asgi)
├── portal/               # Aplicación: modelos, admin, vista y fixture inicial
│   └── fixtures/initial_data.json
├── static/
│   ├── css/styles.css    # Toda la presentación, el movimiento y la interactividad
│   └── img/              # favicon.svg, juzgado.svg, mundo.svg
└── templates/
    ├── base.html
    └── portal/index.html
```

## Puesta en marcha en local

```bash
# 1. Entorno virtual
python -m venv .venv
source .venv/bin/activate            # Windows (PowerShell): .venv\Scripts\Activate.ps1

# 2. Dependencias
pip install -r requirements.txt

# 3. Modo desarrollo
export DJANGO_DEBUG=1                # Windows (PowerShell): $env:DJANGO_DEBUG = "1"

# 4. Base de datos y contenido inicial
python manage.py makemigrations portal
python manage.py migrate
python manage.py loaddata initial_data

# 5. Usuario administrador y servidor
python manage.py createsuperuser
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>. El panel está en <http://127.0.0.1:8000/admin/>.

**Migraciones.** El repositorio no incluye `portal/migrations/`; el paso `makemigrations portal` las genera. Tras el primer arranque, añade esa carpeta a Git (`git add portal/migrations`) para que todos los entornos compartan el mismo esquema y para poder versionar futuros cambios de modelos.

## Variables de entorno

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DJANGO_SECRET_KEY` | En producción | Clave secreta larga y aleatoria. |
| `DJANGO_DEBUG` | No | `1` solo en desarrollo. Por defecto, desactivado. |
| `DJANGO_ALLOWED_HOSTS` | En producción | Dominios separados por comas. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Si hay HTTPS | Orígenes con esquema, p. ej. `https://midominio.es`. |
| `DJANGO_HTTPS` | Recomendada | `1` activa redirección a HTTPS, cookies seguras y HSTS. |
| `DJANGO_ADMIN_URL` | No | Ruta del panel (por defecto `admin/`). |
| `DJANGO_DB_PATH` | No | Ruta del fichero SQLite (por defecto `db.sqlite3`). |
| `DJANGO_LOG_LEVEL` | No | Nivel de registro (por defecto `INFO`). |

Generar una clave secreta:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

## Despliegue

```bash
pip install -r requirements.txt
python manage.py makemigrations portal      # solo si aún no has versionado las migraciones
python manage.py migrate
python manage.py loaddata initial_data      # solo la primera vez
python manage.py collectstatic --noinput
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

Los estáticos los sirve WhiteNoise, por lo que no hace falta configurar Nginx para ellos. Ejemplo de entorno de producción:

```bash
export DJANGO_SECRET_KEY="..."
export DJANGO_ALLOWED_HOSTS="adrianalara.example,www.adrianalara.example"
export DJANGO_CSRF_TRUSTED_ORIGINS="https://adrianalara.example,https://www.adrianalara.example"
export DJANGO_HTTPS=1
```

Con SQLite, el fichero de base de datos debe residir en un almacenamiento persistente (usa `DJANGO_DB_PATH`). Puedes comprobar la configuración con `python manage.py check --deploy`.

## Gestión de contenidos

Desde el panel de administración:

- **Perfil profesional.** Nombre, titular, presentación, sello de la ficha (por defecto «Próxima graduación»; vacío lo oculta), número de colegiada, datos de contacto, lemas de las dos franjas de imagen y aviso legal. Es un registro único.
- **Áreas de interés profesional.** Título, resumen, descripción, ámbito, orden y visibilidad. Alimentan la marquesina y el acordeón filtrable.
- **Criterios de trabajo.** Los cuatro bloques de la sección «Enfoque de trabajo».
- **Hitos de formación y trayectoria.** Formación, trayectoria e investigación, agrupados por categoría.

Cuando un valor está entre corchetes (`[… / Editable]`), la web lo muestra con un realce visual que indica que es provisional. Al sustituirlo por el dato real, el realce desaparece.

**Contenido inicial.** La fixture `initial_data.json` contiene textos de ejemplo redactados en términos generales (áreas, criterios de trabajo, lemas) y marcadores provisionales de formación. Deben revisarse y adaptarse antes de publicar; no se ha incluido ninguna titulación, institución ni fecha.

**Frases de la portada.** Las cuatro frases que se escriben en la portada están en `templates/portal/index.html`. Si cambias su longitud, ajusta la variable `--n` (número de caracteres) de la regla correspondiente `.escribe__frase:nth-child(...)` en el CSS.

## Añadir un ámbito nuevo al filtro

Los ámbitos están definidos en `AreaEstudio.Ambito` (`portal/models.py`). Para añadir uno, crea la clave allí y añade su regla en la sección 8 de `static/css/styles.css`, siguiendo el patrón de las tres existentes.

## Comprobación de «cero JavaScript»

```bash
grep -rniE "<script|onclick|onload|onchange|javascript:" templates static || echo "Sin JavaScript"
find templates static -name "*.js"
```

Ambos comandos deben quedar sin resultados.
