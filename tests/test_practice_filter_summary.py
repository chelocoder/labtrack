import pytest

from test_app import cliente  # Reutiliza el fixture que restaura la lista entre pruebas.


@pytest.mark.parametrize(("query", "expected"), [
    pytest.param({"curso": "Base de Datos"}, {"total": 1, "pendientes": 1, "completadas": 0}, id="CP26-curso"),
    pytest.param({"estado": "completada"}, {"total": 1, "pendientes": 0, "completadas": 1}, id="CP26-estado"),
    pytest.param({"curso": "Base de Datos", "estado": "completada"}, {"total": 0, "pendientes": 0, "completadas": 0}, id="CP26-sin-coincidencias"),
])
def test_resumen_de_la_coleccion_filtrada(cliente, query, expected):
    respuesta = cliente.get("/api/practicas", query_string={**query, "resumen": "true"})

    assert respuesta.status_code == 200
    assert respuesta.get_json() == expected


def test_resumen_filtrado_cambia_al_completar(cliente):
    assert cliente.patch("/api/practicas/1").status_code == 200
    respuesta = cliente.get("/api/practicas?estado=pendiente&resumen=true")

    assert respuesta.status_code == 200
    assert respuesta.get_json() == {"total": 0, "pendientes": 0, "completadas": 0}
