# app.py
# GuarachaCam PRO - Con grabación simulada y envío real a Telegram
# Autor: Rafael Rivas Ramón

import os
import cv2
import threading
import numpy as np
from flask import Flask, Response, render_template_string, redirect, request
from RRR_envio_alerta import enviar_alerta

app = Flask(__name__)
grabando = False
alerta_pendiente = False
mensaje_enviado = False

frame_demo = np.zeros((360, 640, 3), dtype=np.uint8)
cv2.putText(frame_demo, 'GUARACHACAM', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
cv2.putText(frame_demo, 'Render Activo', (40, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

def render_pagina():
    extra_button = ""
    if alerta_pendiente:
        extra_button += """
        <br><br>
        <form action='/enviar_alerta' method='post'>
            <button type='submit'>📤 Enviar alerta a Telegram</button>
        </form>
        """
    if mensaje_enviado:
        extra_button += """
        <p style='color: green; font-weight: bold;'>✅ Alerta enviada correctamente</p>
        """
    return """
    <h2>🎥 GuarachaCam Render - PRO</h2>
    <div id="loading">
        <p>⏳ Cargando GuarachaCam... Por favor, espera un momento.</p>
    </div>
    <img id="video-stream" src='/video' style="display:none;">
    <br><br>
    <form action='/iniciar'>
        <button type='submit'>🎬 Iniciar Grabación</button>
    </form>
    <form action='/detener'>
        <button type='submit'>🛑 Detener Grabación</button>
    </form>
    """ + extra_button + """
    <script>
        const video = document.getElementById('video-stream');
        const loading = document.getElementById('loading');
        video.onload = function() {
            loading.style.display = 'none';
            video.style.display = 'block';
        }
    </script>
    """

def grabar_video():
    global grabando, grabador
    print("[INFO] 🎬 Iniciando grabación...", flush=True)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    grabador = cv2.VideoWriter('guarachacam.avi', fourcc, 20.0, (640, 360))

    if not grabador.isOpened():
        print("[ERROR] ❌ No se pudo abrir el archivo de video.", flush=True)
        grabando = False
        return

    while grabando:
        grabador.write(frame_demo)

    grabador.release()
    print("[INFO] 🎥 Grabación finalizada. Archivo guarachacam.avi creado.", flush=True)

def generate_frames():
    _, buffer = cv2.imencode('.jpg', frame_demo)
    image_bytes = buffer.tobytes()
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template_string(render_pagina())

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/iniciar')
def iniciar_grabacion():
    global grabando, mensaje_enviado
    grabando = True
    mensaje_enviado = False
    threading.Thread(target=grabar_video, daemon=True).start()
    return redirect('/')

@app.route('/detener')
def detener_grabacion():
    global grabando, alerta_pendiente
    if grabando:
        grabando = False
        alerta_pendiente = True
        print("[INFO] 🛑 Grabación detenida. Pendiente enviar alerta.", flush=True)
    return redirect('/')

@app.route('/enviar_alerta', methods=['POST'])
def enviar_alerta_telegram():
    global alerta_pendiente, mensaje_enviado
    if alerta_pendiente:
        alerta_pendiente = False
        mensaje_enviado = True
        enviar_alerta(
            "🚨 *ALERTA GUARACHACAM*\n🎥 Movimiento detectado.\n📁 Archivo: `guarachacam.avi`\n🔔 Estado: Finalizado y en revisión."
        )
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
