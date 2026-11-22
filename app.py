"""Interfaz web (Flask). Sin base de datos: el estado de cada conversación viaja con el navegador."""
import logging
import os

from flask import Flask, jsonify, render_template, request

from chatbot.datos import cargar
from chatbot.logica import SUGERENCIAS, responder

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024  # rechaza peticiones enormes
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING"))  # no se registran mensajes de clientes
NEG = cargar()


@app.get("/")
def inicio():
    return render_template("index.html", neg=NEG, sugerencias=SUGERENCIAS)


@app.post("/chat")
def chat():
    datos = request.get_json(silent=True) or {}
    estado = datos.get("estado") if isinstance(datos.get("estado"), dict) else {}
    return jsonify(responder(datos.get("mensaje"), estado))


@app.errorhandler(Exception)
def error_general(e):
    app.logger.error("Error interno: %s", type(e).__name__)
    return jsonify({"respuesta": "Algo salió mal de nuestro lado. Intenta de nuevo en un momento o escríbenos por WhatsApp.",
                    "fuente": None, "estado": {}}), 200


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", port=int(os.environ.get("PORT", 5000)))
