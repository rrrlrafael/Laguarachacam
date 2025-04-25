# RRR_envio_alerta.py
# Autor: Rafael Rivas Ramón

import requests
import json

# Reemplaza esto con tu token real de BotFather
TOKEN = "TU_TOKEN_DE_TELEGRAM"

def enviar_alerta(mensaje):
    try:
        with open("usuarios_telegram.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
        print("[INFO] ✅ usuarios_telegram.json cargado:", usuarios)
    except Exception as e:
        print(f"[ERROR] ❌ No se pudo leer usuarios_telegram.json: {e}")
        return

    for usuario in usuarios:
        user_id = usuario.get("user_id")
        username = usuario.get("username", "Desconocido")

        print(f"[INFO] 🔄 Intentando enviar mensaje a @{username} (ID: {user_id})")

        if user_id:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            data = {
                "chat_id": user_id,
                "text": mensaje,
                "parse_mode": "Markdown"
            }

            try:
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    print(f"[INFO] ✅ Mensaje enviado correctamente a @{username} ({user_id})")
                else:
                    print(f"[ERROR] ❌ Error enviando a @{username} ({user_id}): {response.text}")
            except Exception as ex:
                print(f"[ERROR] ❌ Excepción enviando a @{username} ({user_id}): {ex}")
