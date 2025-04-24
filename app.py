# app.py
# GuarachaCam para Render con grabación temporal + alerta automática
# Autor: Rafael Rivas Ramón

import os
import cv2
import threading
import numpy as np
from flask import Flask, Response, render_template_string, redirect
from RRR_envio_alerta import enviar_alerta

app = Flask(__name__)
grabando = False
grabador = None

frame_demo = np.zeros((360, 640, 3), dtype=np.uint8)
cv2.putText(frame_demo, 'GUARACHACAM', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
cv2.putText(frame_demo, 'Render Activo', (40, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

HTML_PAGINA = """
<h2>🎥 GuarachaCam Render</h2>
<img src='/video'>
<br><br>
<form action='/iniciar'>
    <button type='submit'>🎬 Iniciar Grabación</button>
</form>
<form action='/detener'>
    <button type='submit'>🛑 Detener y Enviar Alerta</button>
</form>
"""

def grabar_video():
    global grabando, grabador
    print("[INFO] Iniciando grabación...")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    grabador = cv2.VideoWriter('guarachacam.avi', fourcc, 20.0, (640, 360))

    if not grabador.isOpened():
        print("[ERROR] No se pudo abrir el archivo de video.")
        grabando = False
        return

    while grabando:
        grabador.write(frame_demo)

    grabador.release()
    print("[INFO] Grabación finalizada.")

def generate_frames():
    _, buffer = cv2.imencode('.jpg', frame_demo)
    image_bytes = buffer.tobytes()
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML_PAGINA)

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/iniciar')
def iniciar_grabacion():
    global grabando
    if not grabando:
        grabando = True
        threading.Thread(target=grabar_video, daemon=True).start()
    return redirect('/')

@app.route('/detener')
def detener_grabacion():
    global grabando
    if grabando:
        grabando = False
        print("[INFO] Grabación detenida.")
        enviar_alerta("🎥 ¡Grabación finalizada en GuarachaCam Render!")
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
