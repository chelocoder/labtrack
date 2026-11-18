import pytest

from test_app import cliente  # Reutiliza el fixture que restaura la lista entre pruebas.


def test_resumen_inicial(cliente):
    respuesta = cliente.get("/api/practicas?resumen=true")

    assert respuesta.status_code == 200
    assert respuesta.get_json() == {"total": 2, "pendientes": 1, "completadas": 1}


def test_resumen_falso_preserva_la_lista(cliente):
    respuesta = cliente.get("/api/practicas?resumen=false")

    assert respuesta.status_code == 200
    assert respuesta.get_json() == cliente.get("/api/practicas").get_json()


@pytest.mark.parametrize("query", ["resumen=", "resumen=1", "resumen=true&resumen=false"])
def test_resumen_invalido(cliente, query):
    respuesta = cliente.get("/api/practicas?" + query)

    assert respuesta.status_code == 400
    assert respuesta.get_json() == {"error": "El parámetro resumen debe ser true o false"}


def test_resumen_refleja_finalizacion(cliente):
    assert cliente.patch("/api/practicas/1").status_code == 200
    respuesta = cliente.get("/api/practicas?resumen=true")

    assert respuesta.status_code == 200
    assert respuesta.get_json() == {"total": 2, "pendientes": 0, "completadas": 2}
