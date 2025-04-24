# RRR_envio_alerta.py
# Autor: Rafael Rivas Ramón

import requests
import json

TOKEN = "TU_TOKEN_DE_TELEGRAM"  # <-- reemplaza por tu token real

def enviar_alerta(mensaje):
    try:
        with open("usuarios_telegram.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except Exception as e:
        print(f"[ERROR] No se pudo leer usuarios_telegram.json: {e}")
        return

    for usuario in usuarios:
        user_id = usuario.get("user_id")
        username = usuario.get("username", "Desconocido")

        if user_id:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            data = {
                "chat_id": user_id,
                "text": mensaje
            }

            try:
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    print(f"[INFO] ✅ Mensaje enviado a @{username} ({user_id})")
                else:
                    print(f"[ERROR] ❌ Fallo con @{username}: {response.text}")
            except Exception as ex:
                print(f"[ERROR] ❌ Error de conexión con @{username}: {ex}")
