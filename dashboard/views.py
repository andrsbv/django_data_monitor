from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
import requests

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)
def index(request):
    # 1) Traer dato externo (ej.: JSONPlaceholder) para el indicador
    total_responses = 0
    try:
        resp = requests.get(getattr(settings, "API_URL", "https://jsonplaceholder.typicode.com/posts"), timeout=5)
        posts = resp.json()
        total_responses = len(posts)
    except Exception:
        # Si la API falla, nos quedamos con 0
        total_responses = 0

    # 2) Arreglo de filas para la TABLA (SSR)
    rows = [
        {"col1": "fila.valor1", "col2": "fila.valor2"},
        {"col1": "fila.valor3", "col2": ""},
        {"col1": "fila.valor4", "col2": "fila.valor5"},
    ]

    # 3) Datos para el GRÁFICO (SSR)
    chart_labels = ["Hito 1", "Hito 2", "Hito 3", "Hito 4", "Hito 5", "Hito 6", "Hito 7"]
    series_a = [25, 48, 62, 72, 50, 50, 66]
    series_b = [42, 48, 40, 55, 66, 72, 70]

    context = {
        "title": "Landing Page' Dashboard",
        "total_responses": total_responses,   # Indicador 1
        "rows": rows,                         # Tabla (iteración con {% for %})
        "chart_labels": chart_labels,         # Gráfico (inyectado como JSON seguro)
        "series_a": series_a,
        "series_b": series_b,
    }
    return render(request, "dashboard/index.html", context)
