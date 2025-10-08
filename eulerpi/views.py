from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import random

# Cargamos los archivos y dejamos SOLO los decimales (excluimos el "3" de π y el "2" de e)
RAW_PI = (settings.BASE_DIR / 'digits' / 'pi.txt').read_text(encoding='utf-8').replace('.', '').strip()
RAW_E  = (settings.BASE_DIR / 'digits' / 'e.txt').read_text(encoding='utf-8').replace('.', '').strip()

PI_DEC = RAW_PI[1:]  # desde el primer decimal
E_DEC  = RAW_E[1:]   # desde el primer decimal

def index(request):
    return render(request, 'eulerpi/index.html')

def game(request, number):
    digits = PI_DEC if number == "pi" else E_DEC

    # rango opcional por querystring
    min_pos = int(request.GET.get("min", 1))
    max_pos = int(request.GET.get("max", len(digits)))

    # sanitizar rango
    if min_pos < 1: min_pos = 1
    if max_pos > len(digits): max_pos = len(digits)
    if min_pos > max_pos: min_pos, max_pos = max_pos, min_pos

    # posición aleatoria dentro del rango
    position = random.randint(min_pos, max_pos)

    # Para euler: preparamos filas de 100 (hasta 100.000 dígitos)
# ... dentro de def game(request, number):
    rows = []
    if number == "euler":
        dec = digits[:100_000]  # primeros 100.000 decimales
        for i in range(0, len(dec), 100):
            start = i + 1                   # 1-index (primer decimal)
            chunk = dec[i:i+100]            # string con 100 dígitos (o menos en la última)
            end = start + len(chunk) - 1
            rows.append((start, end, chunk))  # <-- ahora guardamos (inicio, fin, trozo)

    return render(request, 'eulerpi/game.html', {
        'number': number,
        'position': position,   # posición actual del desafío (1-index)
        'min_pos': min_pos,
        'max_pos': max_pos,
        'rows': rows,           # lista [(inicio_fila, "100 dígitos"), ...] solo si es euler
    })

def check(request):
    number = request.GET.get('number')
    position = int(request.GET.get('position'))
    guess = request.GET.get('guess', '')

    digits = PI_DEC if number == 'pi' else E_DEC
    # position es 1-index → índice real = position - 1
    correct = digits[position - 1]

    return JsonResponse({'correct': guess == correct, 'expected': correct})
