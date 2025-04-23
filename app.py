 """
app.py (Demo sin cámara física)
Simula transmisión de video con una imagen fija para Render
Autor: Rafael Rivas Ramón
"""

import os
from flask import Flask, Response
import cv2
import numpy as np

app = Flask(__name__)

# Crear una imagen de prueba (negra con texto)
frame = np.zeros((360, 640, 3), dtype=np.uint8)
cv2.putText(frame, 'GuarachaCam DEMO', (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

def generate_frames():
    _, buffer = cv2.imencode('.jpg', frame)
    image_bytes = buffer.tobytes()
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')

@app.route('/')
def index():
    return "<h2>🔴 DEMO en Vivo de GuarachaCam</h2><img src='/video'>"

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
