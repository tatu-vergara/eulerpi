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
    # para el juego usamos TODOS los decimales para validar;
    # para la grilla de e mostramos solo los primeros 10.000
    digits_all = PI_DEC if number == "pi" else E_DEC

    # rango solicitado
    min_pos = int(request.GET.get("min", 1))
    max_pos = int(request.GET.get("max", len(digits_all)))
    if min_pos < 1: min_pos = 1
    if max_pos > len(digits_all): max_pos = len(digits_all)
    if min_pos > max_pos: min_pos, max_pos = max_pos, min_pos

    # posición aleatoria dentro del rango
    position = random.randint(min_pos, max_pos)

    # grilla SOLO para e (10.000 dígitos, 100 columnas x 100 filas)
    rows = []
    col_headers = list(range(1, 101))
    shown_len = 0
    if number == "euler":
        dec = E_DEC[:10_000]
        shown_len = len(dec)
        for i in range(0, shown_len, 100):
            start = i + 1                 # 1-index (primer decimal)
            chunk = dec[i:i+100]          # string (hasta 100 chars)
            end = start + len(chunk) - 1
            rows.append((start, end, chunk))  # (inicio, fin, trozo)

    return render(request, 'eulerpi/game.html', {
        "number": number,
        "position": position,     # posición preguntada
        "min_pos": min_pos,
        "max_pos": max_pos,
        "rows": rows,             # filas euler (si aplica)
        "col_headers": col_headers,
        "shown_len": shown_len,   # largo de la grilla (<=10.000)
    })

def check(request):
    number = request.GET.get('number')
    position = int(request.GET.get('position'))
    guess = request.GET.get('guess', '')

    digits = PI_DEC if number == 'pi' else E_DEC
    correct = digits[position - 1]  # 1-index → índice real - 1

    return JsonResponse({"correct": guess == correct, "expected": correct})
