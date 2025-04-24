"""
app.py
GuarachaCam DEMO con rastreo completo del proceso de grabación
Autor: Rafael Rivas Ramón
"""

import os
import cv2
import threading
import numpy as np
from flask import Flask, Response, render_template_string, redirect

app = Flask(__name__)

grabando = False
grabador = None

# Crear imagen DEMO con marca de agua
frame_demo = np.zeros((360, 640, 3), dtype=np.uint8)
cv2.putText(frame_demo, 'SABROSO EN VIVO', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
cv2.putText(frame_demo, 'Rastreo Activo', (40, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

# HTML con botones
HTML_PAGINA = """
<h2>🎥 GuarachaCam DEMO - Rastreo</h2>
<img src='/video'>
<br><br>
<form action='/iniciar'>
    <button type='submit'>🎬 Iniciar Grabación</button>
</form>
<form action='/detener'>
    <button type='submit'>🛑 Detener Grabación</button>
</form>
"""

def grabar_video():
    global grabando, grabador
    print("[INFO] Entrando a grabar_video()...")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    grabador = cv2.VideoWriter('guarachacam.avi', fourcc, 20.0, (640, 360))

    if not grabador.isOpened():
        print("[ERROR] No se pudo abrir el archivo de video para grabar.")
        grabando = False
        return

    print("[INFO] Grabación iniciada correctamente.")
    while grabando:
        grabador.write(frame_demo)
        print("[INFO] Frame grabado...")

    grabador.release()
    print("[INFO] Grabación finalizada y archivo guardado.")

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
    print("[INFO] Ruta /iniciar llamada.")
    if not grabando:
        print("[INFO] Estado grabando = False. Iniciando hilo de grabación...")
        grabando = True
        t = threading.Thread(target=grabar_video)
        t.daemon = True
        t.start()
    else:
        print("[INFO] Ya se estaba grabando.")
    return redirect('/')

@app.route('/detener')
def detener_grabacion():
    global grabando
    print("[INFO] Ruta /detener llamada.")
    if grabando:
        grabando = False
        print("[INFO] Grabación detenida por usuario.")
    else:
        print("[INFO] Ya estaba detenido.")
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"[INFO] Servidor Flask iniciado en puerto {port}")
    app.run(host='0.0.0.0', port=port)
