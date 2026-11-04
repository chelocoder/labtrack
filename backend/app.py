
from flask import Flask, jsonify, request
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

@app.post("/api/practicas")
def registrar_practica():
    """Registra una nueva práctica de aprendizaje."""
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Se requiere un objeto JSON válido"}), 400

    titulo = datos.get("titulo")
    curso = datos.get("curso")

    if not isinstance(titulo, str) or not titulo.strip():
        return jsonify({"error": "El título es obligatorio"}), 400

    if not isinstance(curso, str) or not curso.strip():
        return jsonify({"error": "El curso es obligatorio"}), 400

    nuevo_id = max((p["id"] for p in practicas), default=0) + 1

    nueva_practica = {
        "id": nuevo_id,
        "titulo": titulo.strip(),
        "curso": curso.strip(),
        "completada": False
    }

    practicas.append(nueva_practica)

    return jsonify(nueva_practica), 201

if __name__ == "__main__":
    app.run(debug=True)
