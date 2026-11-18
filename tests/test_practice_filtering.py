import pytest

from test_app import cliente  # Reutiliza el fixture que restaura la lista entre pruebas.


@pytest.mark.parametrize(("query", "ids"), [
    pytest.param({"curso": "  BASE de datos  "}, [1], id="CP18-curso"),
    pytest.param({"estado": "pendiente"}, [1], id="CP19-pendiente"),
    pytest.param({"estado": " COMPLETADA "}, [2], id="CP19-completada"),
    pytest.param({"curso": "Ingeniería de Software", "estado": "pendiente"}, [], id="CP20-and"),
    pytest.param({"curso": "Otro curso"}, [], id="CP20-sin-coincidencias"),
])
def test_filtrado_valido(cliente, query, ids):
    respuesta = cliente.get("/api/practicas", query_string=query)

    assert respuesta.status_code == 200
    assert [p["id"] for p in respuesta.get_json()] == ids


@pytest.mark.parametrize("query", [
    pytest.param([("curso", " ")], id="CP21-curso-vacio"),
    pytest.param([("estado", "cerrada")], id="CP21-estado-invalido"),
    pytest.param([("curso", "a"), ("curso", "b")], id="CP21-curso-repetido"),
    pytest.param([("estado", "pendiente"), ("estado", "completada")], id="CP21-estado-repetido"),
])
def test_filtro_invalido_no_modifica_listado(cliente, query):
    antes = cliente.get("/api/practicas").get_json()
    respuesta = cliente.get("/api/practicas", query_string=query)

    assert respuesta.status_code == 400
    assert respuesta.get_json()["error"]
    assert cliente.get("/api/practicas").get_json() == antes
