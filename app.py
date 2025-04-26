from flask import Flask, render_template, Response
import cv2
import os
from datetime import datetime

app = Flask(__name__)

# Variables globales
cap = cv2.VideoCapture(0)
grabando = False
out = None

@app.route('/')
def index():
    # Aquí cambiamos para que use rrr_index.html
    return render_template('rrr_index.html')

@app.route('/video_feed')
def video_feed():
    def gen():
        global cap, grabando, out

        while True:
            success, frame = cap.read()
            if not success:
                break

            if grabando and out is not None:
                out.write(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/iniciar_grabacion')
def iniciar_grabacion():
    global grabando, out

    carpeta_videos = "videos_guardados"
    if not os.path.exists(carpeta_videos):
        os.makedirs(carpeta_videos)

    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"guarachacam_{fecha_hora}.mp4"
    ruta_completa = os.path.join(carpeta_videos, nombre_archivo)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 20.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(ruta_completa, fourcc, fps, (width, height))
    grabando = True
    print(f"[GUARACHACAM] 🎥 Grabando video en: {ruta_completa}")
    return "Grabación iniciada"

@app.route('/detener_grabacion')
def detener_grabacion():
    global grabando, out

    if grabando and out is not None:
        grabando = False
        out.release()
        out = None
        print("[GUARACHACAM] 🛑 Grabación detenida y archivo guardado.")
    return "Grabación detenida"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
