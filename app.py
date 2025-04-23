"""
app.py
GuarachaCam con transmisión en vivo + control de grabación desde botones
Autor: Rafael Rivas Ramón
"""

import os
import cv2
import threading
from flask import Flask, Response, render_template_string, redirect

app = Flask(__name__)

camera = cv2.VideoCapture(0)
grabando = False
grabador = None

# HTML de la interfaz con botones
HTML_PAGINA = """
<h2>🎥 GuarachaCam en Vivo</h2>
<img src='/video'>
<br><br>
<form action='/iniciar'>
    <button type='submit'>🎬 Iniciar Grabación</button>
</form>
<form action='/detener'>
    <button type='submit'>🛑 Detener Grabación</button>
</form>
"""

# Grabar en segundo plano
def grabar_video():
    global grabando, grabador
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    grabador = cv2.VideoWriter('guarachacam.avi', fourcc, 20.0, (640, 480))
    while grabando:
        ret, frame = camera.read()
        if ret:
            grabador.write(frame)
    grabador.release()

# Transmisión en vivo
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
