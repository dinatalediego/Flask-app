from flask import Flask, request, jsonify
import os
import requests
import random
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

app = Flask(__name__)

class Translator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api-free.deepl.com/v2/translate"

    def traducir(self, texto, source_lang='EN', target_lang='DE'):
        params = {
            'auth_key': self.api_key,
            'text': texto,
            'source_lang': source_lang,
            'target_lang': target_lang
        }
        try:
            response = requests.post(self.api_url, data=params, verify=False)
            response.raise_for_status()
            result = response.json()
            return result['translations'][0]['text']
        except requests.exceptions.RequestException as req_err:
            print(f"Error en la traducción: {req_err}")
            return "Error en la traducción"


# Instanciar el traductor
translator = Translator(DEEPL_API_KEY)

# Preguntas A/B iniciales
preguntas_ab = ["¿Te gusta aprender alemán? A) Ja, B) Nein", 
                "¿Prefieres leer o escuchar? A) Lesen, B) Hören"]

@app.route('/traducir', methods=['POST'])
def traducir_texto():
    data = request.get_json()
    texto = data.get('texto')
    
    if not texto:
        return jsonify({'error': 'No se envió texto para traducir.'}), 400
    
    # Traducir texto del inglés al alemán
    traducido = translator.traducir(texto, 'EN', 'DE')
    
    return jsonify({'texto_traducido': traducido})

@app.route('/respuesta', methods=['GET'])
def generar_respuesta():
    # Ejemplos de respuestas en alemán
    respuestas_amigo = [
        "Das ist interessant!",
        "Ich finde das toll.",
        "Das verstehe ich.",
        "Was denkst du darüber?",
        "Kannst du mehr darüber erzählen?"
    ]
    respuesta = random.choice(respuestas_amigo)
    
    # Generar una pregunta A/B aleatoria
    pregunta = random.choice(preguntas_ab)
    
    return jsonify({'respuesta': respuesta, 'pregunta': pregunta})

if __name__ != "__main__":
    app = app
