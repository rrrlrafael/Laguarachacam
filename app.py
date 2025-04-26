# app.py
# GuarachaCam Ultra Básico - Botones con flush sabroso
# Autor: Rafael Rivas Ramón

import os
from flask import Flask, render_template_string, redirect, request

app = Flask(__name__)
grabando = False
alerta_pendiente = False

def render_pagina():
    extra_button = ""
    if alerta_pendiente:
        extra_button = """
        <br><br>
        <form action='/enviar_alerta' method='post'>
            <button type='submit'>📤 Enviar alerta a Telegram</button>
        </form>
        """
    return """
    <h2>🎥 GuarachaCam Render (Modo Prueba de Botones)</h2>
    <div id="loading">
        <p>⏳ Cargando GuarachaCam... Por favor, espera un momento.</p>
    </div>
    <img id="video-stream" src='https://via.placeholder.com/640x360?text=GuarachaCam+Demo' style="display:block;">
    <br><br>
    <form action='/iniciar'>
        <button type='submit'>🎬 Iniciar Grabación</button>
    </form>
    <form action='/detener'>
        <button type='submit'>🛑 Detener Grabación</button>
    </form>
    """ + extra_button + """
    <script>
        const loading = document.getElementById('loading');
        loading.style.display = 'none';
    </script>
    """

@app.route('/')
def index():
    return render_template_string(render_pagina())

@app.route('/iniciar')
def iniciar_grabacion():
    global grabando
    grabando = True
    print("[INFO] 🎬 Botón INICIAR presionado.", flush=True)
    return redirect('/')

@app.route('/detener')
def detener_grabacion():
    global grabando, alerta_pendiente
    if grabando:
        grabando = False
        alerta_pendiente = True
        print("[INFO] 🛑 Botón DETENER presionado.", flush=True)
    return redirect('/')

@app.route('/enviar_alerta', methods=['POST'])
def enviar_alerta_telegram():
    global alerta_pendiente
    if alerta_pendiente:
        alerta_pendiente = False
        print("[INFO] 📤 Botón ENVIAR ALERTA presionado.", flush=True)
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
