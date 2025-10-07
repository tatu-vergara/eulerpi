from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import random

# Carga los dígitos (quitamos el punto decimal)
PI = (settings.BASE_DIR / 'digits' / 'pi.txt').read_text(encoding='utf-8').replace('.', '').strip()
E  = (settings.BASE_DIR / 'digits' / 'e.txt').read_text(encoding='utf-8').replace('.', '').strip()

def index(request):
    return render(request, 'eulerpi/index.html')

# ✅ FUNCIÓN ACTUALIZADA
def game(request, number):
    digits = PI if number == "pi" else E

    # obtener rango desde la url o usar valores por defecto
    min_pos = int(request.GET.get("min", 1))
    max_pos = int(request.GET.get("max", len(digits)))

    # validar rango
    if min_pos < 1:
        min_pos = 1
    if max_pos > len(digits):
        max_pos = len(digits)
    if min_pos > max_pos:
        min_pos, max_pos = max_pos, min_pos  # invertir si el usuario lo escribió al revés

    # generar número aleatorio dentro del rango
    position = random.randint(min_pos, max_pos)

    return render(request, 'eulerpi/game.html', {
        'number': number,
        'position': position,
        'min_pos': min_pos,
        'max_pos': max_pos,
    })

def check(request):
    number = request.GET.get('number')
    position = int(request.GET.get('position'))
    guess = request.GET.get('guess', '')

    digits = PI if number == 'pi' else E
    correct = digits[position - 1]

    return JsonResponse({
        'correct': guess == correct,
        'expected': correct
    })
