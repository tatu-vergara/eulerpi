from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
import random

# --- Carga de dígitos (quitamos el entero inicial) ---
RAW_PI = (settings.BASE_DIR / 'digits' / 'pi.txt').read_text(encoding='utf-8').replace('.', '').strip()
RAW_E  = (settings.BASE_DIR / 'digits' / 'e.txt').read_text(encoding='utf-8').replace('.', '').strip()

PI_DEC = RAW_PI[1:]   # solo decimales
E_DEC  = RAW_E[1:]

MAX_DECIMALS_DEFAULT = 10_000  # tope por defecto

def index(request):
    return render(request, 'eulerpi/index.html')

def game(request, number: str):
    digits_all = PI_DEC if number == "pi" else E_DEC

    # Topes por defecto: 1..min(10k, largo real)
    max_default = min(MAX_DECIMALS_DEFAULT, len(digits_all))

    # Rango pedido (si no viene, usamos el tope por defecto)
    min_pos = int(request.GET.get("min", 1))
    max_pos = int(request.GET.get("max", max_default))

    # Clampeamos SIEMPRE a 1..max_default (evita 51.700, etc.)
    if min_pos < 1: min_pos = 1
    if max_pos > max_default: max_pos = max_default
    if min_pos > max_pos: min_pos, max_pos = max_pos, min_pos

    # Posición aleatoria dentro del rango
    position = random.randint(min_pos, max_pos)

    # Grilla SOLO para e: 10.000 (o menos, si el archivo es más corto)
    rows = []
    col_headers = list(range(1, 101))
    shown_len = 0
    if number == "euler":
        dec = digits_all[:max_default]
        shown_len = len(dec)  # normalmente 10.000
        # 100 columnas por fila → bloques de 100
        for i in range(0, shown_len, 100):
            start = i + 1
            chunk = list(dec[i:i+100])  # lista de caracteres
            end = start + len(chunk) - 1
            rows.append({"start": start, "end": end, "chunk": chunk})

    return render(request, 'eulerpi/game.html', {
        "number": number,
        "position": position,
        "min_pos": min_pos,
        "max_pos": max_pos,
        "rows": rows,                 # solo para e
        "col_headers": col_headers,   # 1..100
        "shown_len": shown_len,       # 10.000
    })

def check(request):
    number = request.GET.get('number')
    position = int(request.GET.get('position'))
    guess = request.GET.get('guess', '')

    digits = PI_DEC if number == 'pi' else E_DEC
    correct = digits[position - 1]  # 1-index

    return JsonResponse({"correct": guess == correct, "expected": correct})
