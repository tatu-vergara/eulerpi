from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import random

# Cargamos los archivos crudos y nos quedamos con los DECIMALES (excluye el entero)
RAW_PI = (settings.BASE_DIR / 'digits' / 'pi.txt').read_text(encoding='utf-8').replace('.', '').strip()
RAW_E  = (settings.BASE_DIR / 'digits' / 'e.txt').read_text(encoding='utf-8').replace('.', '').strip()

PI_DEC = RAW_PI[1:]  # decimales de pi
E_DEC  = RAW_E[1:]   # decimales de e

def index(request):
    return render(request, 'eulerpi/index.html')

def game(request, number: str):
    digits_all = PI_DEC if number == "pi" else E_DEC

    # rango de juego
    min_pos = int(request.GET.get("min", 1))
    max_pos = int(request.GET.get("max", len(digits_all)))
    if min_pos < 1: min_pos = 1
    if max_pos > len(digits_all): max_pos = len(digits_all)
    if min_pos > max_pos: min_pos, max_pos = max_pos, min_pos

    # posición aleatoria
    position = random.randint(min_pos, max_pos)

    # grilla para e: 10.000 decimales => 100 filas x 100 columnas
    rows = []
    col_headers = list(range(1, 101))
    shown_len = 0
    if number == "euler":
        dec = E_DEC[:10_000]              # EXACTO 10.000
        shown_len = len(dec)
        for i in range(0, shown_len, 100):
            start = i + 1
            chunk = list(dec[i:i+100])    # <-- lista de caracteres (no string)
            end = start + len(chunk) - 1
            rows.append({"start": start, "end": end, "chunk": chunk})

    return render(request, 'eulerpi/game.html', {
        "number": number,
        "position": position,
        "min_pos": min_pos,
        "max_pos": max_pos,
        "rows": rows,
        "col_headers": col_headers,
        "shown_len": shown_len,
    })

def check(request):
    number = request.GET.get('number')
    position = int(request.GET.get('position'))
    guess = request.GET.get('guess', '')

    digits = PI_DEC if number == 'pi' else E_DEC
    correct = digits[position - 1]
    return JsonResponse({"correct": guess == correct, "expected": correct})
