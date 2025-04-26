# RRR_envio_alerta.py
# Autor: Rafael Rivas Ramón

import requests
import json
from credenciales import TOKEN, USUARIOS

def enviar_alerta(mensaje):
    usuarios_final = []

    try:
        with open("usuarios_telegram.json", "r", encoding="utf-8") as f:
            usuarios_json = json.load(f)
            usuarios_final = [usuario.get("user_id") for usuario in usuarios_json if usuario.get("user_id")]
            print("[INFO] ✅ usuarios_telegram.json cargado correctamente.", flush=True)
    except Exception as e:
        print(f"[WARN] ⚠️ No se pudo cargar usuarios_telegram.json ({e}), usando USUARIOS de credenciales.py", flush=True)
        usuarios_final = USUARIOS

    for user_id in usuarios_final:
        print(f"[INFO] 🔄 Enviando mensaje a {user_id}", flush=True)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": user_id,
            "text": mensaje,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"[INFO] ✅ Mensaje enviado correctamente a {user_id}", flush=True)
            else:
                print(f"[ERROR] ❌ Fallo enviando a {user_id}: {response.text}", flush=True)
        except Exception as ex:
            print(f"[ERROR] ❌ Excepción enviando a {user_id}: {ex}", flush=True)
