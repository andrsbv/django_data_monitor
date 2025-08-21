import requests
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)
def index(request):
    # Obtener datos desde el API externo
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = response.json()

    # Limitar a los primeros 10 posts para la tabla
    primeros_posts = posts[:10]

    # Preparar filas para la tabla (solo primeros 10)
    filas = [
        {"valor1": f"[{p['id']}] {p['title']}", "valor2": p['body']}
        for p in primeros_posts
    ]

    # Columnas de la tabla
    columnas = ["ID / Título", "Contenido"]

    # Total de respuestas (usamos total de posts originales para indicadores)
    total_respuestas = len(posts)

    # Indicadores para mostrar
    indicadores = [
        {"titulo": "Total de Posts", "valor": total_respuestas},
        {"titulo": "ID mínimo", "valor": min(p['id'] for p in posts)},
        {"titulo": "ID máximo", "valor": max(p['id'] for p in posts)},
        {"titulo": "Long. media del body", "valor": round(sum(len(p['body']) for p in posts) / total_respuestas, 1)},
    ]

    # Datos para gráfico: posts por usuario (todo el dataset)
    conteo_por_usuario = {}
    for p in posts:
        conteo_por_usuario[p['userId']] = conteo_por_usuario.get(p['userId'], 0) + 1

    grafico_data = {
        "labels": [f"Usuario {uid}" for uid in sorted(conteo_por_usuario.keys())],
        "datasets": [{
            "label": "Posts por Usuario",
            "data": [conteo_por_usuario[uid] for uid in sorted(conteo_por_usuario.keys())],
            "backgroundColor": "rgba(59, 130, 246, 0.5)",  # azul claro para barra
            "borderColor": "rgba(59, 130, 246, 1)",
            "borderWidth": 1
        }]
    }
    grafico_data_json = json.dumps(grafico_data)

    # Contexto para renderizar
    context = {
        "titulo_secundario": "DASHBOARD",
        "indicadores": indicadores,
        "columnas": columnas,
        "filas": filas,
        "total_respuestas": total_respuestas,
        "grafico_data_json": grafico_data_json,
    }

    return render(request, "dashboard/index.html", context)