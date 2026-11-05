import copy
import pytest

from backend.app import app
from backend.models import practicas


@pytest.fixture
def cliente():
    """Prepara un cliente HTTP y aísla los datos de cada prueba."""
    datos_originales = copy.deepcopy(practicas)

    app.config["TESTING"] = True

    with app.test_client() as cliente_prueba:
        yield cliente_prueba

    practicas[:] = datos_originales


def test_servidor_disponible(cliente):
    respuesta = cliente.get("/api/salud")

    assert respuesta.status_code == 200
    assert respuesta.get_json()["estado"] == "operativo"


def test_consultar_practicas(cliente):
    respuesta = cliente.get("/api/practicas")

    assert respuesta.status_code == 200
    assert isinstance(respuesta.get_json(), list)
    assert len(respuesta.get_json()) == 2


def test_registrar_practica(cliente):
    nueva_practica = {
        "titulo": "Pruebas automatizadas con pytest",
        "curso": "Ingeniería de Software II"
    }

    respuesta = cliente.post(
        "/api/practicas",
        json=nueva_practica
    )

    datos = respuesta.get_json()

    assert respuesta.status_code == 201
    assert datos["id"] == 3
    assert datos["completada"] is False
    assert len(practicas) == 3


def test_rechazar_practica_sin_titulo(cliente):
    respuesta = cliente.post(
        "/api/practicas",
        json={"titulo": "", "curso": "Backend"}
    )

    assert respuesta.status_code == 400
    assert "error" in respuesta.get_json()


def test_completar_practica(cliente):
    respuesta = cliente.patch("/api/practicas/1")

    assert respuesta.status_code == 200
    assert respuesta.get_json()["completada"] is True


def test_practica_inexistente(cliente):
    respuesta = cliente.patch("/api/practicas/999")

    assert respuesta.status_code == 404
    assert "error" in respuesta.get_json()
