"""
app.py
GuarachaCam DEMO en Render con imagen fija + control de grabación por botones
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

# Crear imagen DEMO negra con texto
frame_demo = np.zeros((360, 640, 3), dtype=np.uint8)
cv2.putText(frame_demo, 'GuarachaCam DEMO', (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

# HTML con botones
HTML_PAGINA = """
<h2>🎥 GuarachaCam en Vivo (DEMO)</h2>
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
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    grabador = cv2.VideoWriter('guarachacam.avi', fourcc, 20.0, (640, 360))
    while grabando:
        grabador.write(frame_demo)
    grabador.release()

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
        threading.Thread(target=grabar_video).start()
    return redirect('/')

@app.route('/detener')
def detener_grabacion():
    global grabando
    grabando = False
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
