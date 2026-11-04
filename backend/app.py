
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/api/salud")
def verificar_salud():
    """Comprueba que el servicio está disponible."""
    return jsonify({
        "aplicacion": "SENATI LabTrack",
        "estado": "operativo",
        "version": "0.1.0"
    })


if __name__ == "__main__":
    app.run(debug=True)
