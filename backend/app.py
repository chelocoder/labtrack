
from flask import Flask, jsonify
from backend.models import practicas

app = Flask(__name__)


@app.get("/api/salud")
def verificar_salud():
    """Comprueba que el servicio está disponible."""
    return jsonify({
        "aplicacion": "SENATI LabTrack",
        "estado": "operativo",
        "version": "0.1.0"
    })


@app.get("/api/practicas")
def consultar_practicas():
    """Devuelve las prácticas de aprendizaje registradas."""
    return jsonify(practicas), 200


if __name__ == "__main__":
    app.run(debug=True)
