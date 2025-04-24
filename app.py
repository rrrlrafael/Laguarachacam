"""
app.py
GuarachaCam DEMO en Render - muestra imagen fija con marca de agua
Autor: Rafael Rivas Ramón
"""

import os
import cv2
import numpy as np
from flask import Flask, Response, render_template_string, redirect

app = Flask(__name__)

# Crear imagen DEMO con marca de agua
frame_demo = np.zeros((360, 640, 3), dtype=np.uint8)
cv2.putText(frame_demo, 'RRR DEMO EN VIVO', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
cv2.putText(frame_demo, 'Probando desde Render', (40, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

# HTML con imagen fija y botones
HTML_PAGINA = """
<h2>🎥 GuarachaCam DEMO - Imagen Fija</h2>
<img src='/foto'>
<br><br>
<form action='/iniciar'>
    <button type='submit'>🎬 Iniciar Grabación</button>
</form>
<form action='/detener'>
    <button type='submit'>🛑 Detener Grabación</button>
</form>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGINA)

@app.route('/foto')
def foto():
    _, buffer = cv2.imencode('.jpg', frame_demo)
    return Response(buffer.tobytes(), mimetype='image/jpeg')

@app.route('/iniciar')
def iniciar_grabacion():
    return redirect('/')

@app.route('/detener')
def detener_grabacion():
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
