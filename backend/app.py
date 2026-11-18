
from flask import Flask, jsonify, request
from backend.models import practicas

MAX_TITULO = 120
MAX_CURSO = 80

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)


@app.get("/api/salud")
def verificar_salud():
    """Comprueba que el servicio está disponible."""
    return jsonify({
        "aplicacion": "LabTrack",
        "estado": "operativo",
        "version": "0.1.0"
    })

@app.get("/")
def pagina_principal():
    """Muestra la interfaz web de SENATI LabTrack."""
    return app.send_static_file("index.html")

@app.get("/api/practicas")
def consultar_practicas():
    """Devuelve las prácticas filtradas o sus cantidades por estado."""
    if any(len(request.args.getlist(campo)) > 1 for campo in ("curso", "estado")):
        return jsonify({"error": "Los filtros curso y estado no admiten valores repetidos"}), 400

    curso = request.args.get("curso")
    estado = request.args.get("estado")
    if curso is not None:
        curso = curso.strip().casefold()
        if not curso:
            return jsonify({"error": "El filtro curso no puede estar vacío"}), 400

    if estado is not None:
        estado = estado.strip().casefold()
        if estado not in ("pendiente", "completada"):
            return jsonify({"error": "El estado debe ser pendiente o completada"}), 400

    resultado = [
        practica for practica in practicas
        if (curso is None or practica["curso"].casefold() == curso)
        and (estado is None or practica["completada"] == (estado == "completada"))
    ]
    return responder_consulta(resultado)


def responder_consulta(registros):
    valores = request.args.getlist("resumen")
    if len(valores) > 1 or (valores and valores[0] not in ("true", "false")):
        return jsonify({"error": "El parámetro resumen debe ser true o false"}), 400

    if valores != ["true"]:
        return jsonify(registros), 200

    completadas = sum(practica["completada"] for practica in registros)
    total = len(registros)
    return jsonify(total=total, pendientes=total - completadas, completadas=completadas), 200

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

    titulo = titulo.strip()
    curso = curso.strip()

    if len(titulo) > MAX_TITULO:
        return jsonify({"error": f"El título admite como máximo {MAX_TITULO} caracteres"}), 400

    if len(curso) > MAX_CURSO:
        return jsonify({"error": f"El curso admite como máximo {MAX_CURSO} caracteres"}), 400

    nuevo_id = max((p["id"] for p in practicas), default=0) + 1

    nueva_practica = {
        "id": nuevo_id,
        "titulo": titulo,
        "curso": curso,
        "completada": False
    }

    practicas.append(nueva_practica)

    return jsonify(nueva_practica), 201

@app.patch("/api/practicas/<int:practica_id>")
def completar_practica(practica_id):
    """Marca una práctica de aprendizaje como completada."""

    practica = next(
        (p for p in practicas if p["id"] == practica_id),
        None
    )

    if practica is None:
        return jsonify({
            "error": "La práctica solicitada no existe"
        }), 404

    practica["completada"] = True

    return jsonify(practica), 200


if __name__ == "__main__":
    app.run(debug=True)
