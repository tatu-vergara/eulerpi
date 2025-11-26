# 🧠 EulerPi — Juego interactivo de memoria numérica  
Aplicación web desarrollada en **Python + Django** que ayuda a entrenar a nemonistas que estén memorizando dígitos de pi y euler.  
Permite practicar Pi y Euler, pudiendo escoger rangos de números al azar 

Demo en línea (Render):  
👉 https://eulerpi.onrender.com/

---

## Funcionalidades principales

- Generación dinámica de secuencias numéricas (Pi, Euler y más).
- Interfaz simple e intuitiva para usuarios nuevos.
- Validación inmediata de respuestas.
- Lógica de juego implementada con Django + vistas personalizadas.
- Versión en vivo desplegada con **Render**.

---

## Tecnologías utilizadas

### **Backend**
- **Python 3**
- **Django 5**
- Django Views & Templates
- Lógica de juego basada en funciones Python

### **Frontend**
- HTML5  
- CSS3  
- JavaScript nativo (validaciones y dinámica del juego)

### **Base de datos**
- SQLite (desarrollo)

### **Deploy**
- **Render.com** (servicio gratuito para proyectos Django)
- Configuración usando `requirements.txt` y `build & start commands` personalizados

---

## Instalación y uso

### 1. Clonar el repositorio

git clone https://github.com/tatu-vergara/eulerpi.git
cd eulerpi

### 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Ejecutar migraciones
python manage.py migrate

### 5. Iniciar el servidor
python manage.py runserver


La aplicación estará disponible en:
http://127.0.0.1:8000/

## Deploy en Render

Este proyecto está desplegado en Render.com utilizando:

Entorno: Web Service

Runtime: Python 3

Build command:

pip install -r requirements.txt


Start command:

gunicorn eulerpi.wsgi


Se utilizó un servicio gratuito, ideal para proyectos Django de demostración.

📁 Estructura del proyecto
eulerpi/
│── eulerpi/          # Configuración principal Django
│── juego/            # App del juego (views, lógica, rutas)
│── templates/        # HTML del proyecto
│── static/           # CSS, JS
│── manage.py
│── requirements.txt

### Licencia

Este proyecto está disponible bajo la licencia MIT.
Puedes usarlo, modificarlo o adaptarlo mencionando la autoría.

✉ Contacto

Portafolio: https://tatu-vergara.github.io/

GitHub: https://github.com/tatu-vergara