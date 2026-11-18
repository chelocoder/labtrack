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


@pytest.mark.parametrize(
    ("titulo", "curso"),
    [
        pytest.param("A" * 120, "Curso", id="CP01-titulo-maximo"),
        pytest.param("Práctica", "B" * 80, id="CP02-curso-maximo"),
        pytest.param("🧪" * 120, "Á" * 80, id="CP03-unicode"),
        pytest.param("A", "B", id="CP04-minimo"),
    ],
)
def test_acepta_longitudes_validas_despues_de_recortar(cliente, titulo, curso):
    respuesta = cliente.post(
        "/api/practicas",
        json={"titulo": f"  {titulo}  ", "curso": f"\t{curso}\n"},
    )

    assert respuesta.status_code == 201
    assert respuesta.get_json() == {
        "id": 3, "titulo": titulo, "curso": curso, "completada": False
    }
    assert cliente.get("/api/practicas").get_json()[-1] == respuesta.get_json()


@pytest.mark.parametrize(
    ("campo", "valor", "mensaje"),
    [
        pytest.param(
            "titulo", "A" * 121, "El título admite como máximo 120 caracteres",
            id="CP05-titulo-excedido",
        ),
        pytest.param(
            "curso", "B" * 81, "El curso admite como máximo 80 caracteres",
            id="CP06-curso-excedido",
        ),
        pytest.param("titulo", " \t\n ", "El título es obligatorio", id="CP07-titulo-blanco"),
        pytest.param("curso", " \t\n ", "El curso es obligatorio", id="CP07-curso-blanco"),
        pytest.param("titulo", 42, "El título es obligatorio", id="CP08-titulo-numero"),
        pytest.param("curso", [], "El curso es obligatorio", id="CP08-curso-arreglo"),
        pytest.param("curso", None, "El curso es obligatorio", id="CP08-curso-nulo"),
        pytest.param("curso", "", "El curso es obligatorio", id="CP07-curso-vacio"),
    ],
)
def test_rechaza_campo_invalido_sin_registrar(cliente, campo, valor, mensaje):
    anterior = cliente.get("/api/practicas").get_json()
    datos = {"titulo": "Práctica", "curso": "Curso"}
    datos[campo] = valor

    respuesta = cliente.post("/api/practicas", json=datos)

    assert respuesta.status_code == 400
    assert respuesta.get_json() == {"error": mensaje}
    assert cliente.get("/api/practicas").get_json() == anterior


def test_rechaza_curso_ausente(cliente):
    anterior = cliente.get("/api/practicas").get_json()
    respuesta = cliente.post("/api/practicas", json={"titulo": "Práctica"})

    assert respuesta.status_code == 400
    assert respuesta.get_json() == {"error": "El curso es obligatorio"}
    assert cliente.get("/api/practicas").get_json() == anterior


@pytest.mark.parametrize(
    ("cuerpo", "tipo"),
    [
        pytest.param("{", "application/json", id="CP10-json-malformado"),
        pytest.param("[]", "application/json", id="CP10-arreglo-json"),
        pytest.param("null", "application/json", id="CP10-json-nulo"),
        pytest.param("{}", "text/plain", id="CP10-tipo-no-json"),
    ],
)
def test_rechaza_cuerpo_que_no_es_objeto_json(cliente, cuerpo, tipo):
    anterior = cliente.get("/api/practicas").get_json()
    respuesta = cliente.post("/api/practicas", data=cuerpo, content_type=tipo)

    assert respuesta.status_code == 400
    assert respuesta.get_json() == {"error": "Se requiere un objeto JSON válido"}
    assert cliente.get("/api/practicas").get_json() == anterior


def test_repetir_actualizacion_conserva_el_mismo_recurso(cliente):
    anterior = cliente.get("/api/practicas").get_json()
    primera = cliente.patch("/api/practicas/1")
    listado = cliente.get("/api/practicas").get_json()

    segunda = cliente.patch("/api/practicas/1")

    assert primera.status_code == segunda.status_code == 200
    assert primera.get_json() == segunda.get_json()
    assert segunda.get_json()["completada"] is True
    assert listado[1:] == anterior[1:]
    assert cliente.get("/api/practicas").get_json() == listado


def test_actualizar_id_desconocido_no_modifica_el_listado(cliente):
    anterior = cliente.get("/api/practicas").get_json()
    respuesta = cliente.patch("/api/practicas/999")

    assert respuesta.status_code == 404
    assert respuesta.get_json() == {"error": "La práctica solicitada no existe"}
    assert cliente.get("/api/practicas").get_json() == anterior


def test_primer_registro_en_lista_vacia_recibe_id_uno(cliente):
    practicas.clear()

    respuesta = cliente.post("/api/practicas", json={"titulo": "Inicio", "curso": "Curso"})

    assert respuesta.status_code == 201
    assert respuesta.get_json()["id"] == 1
    assert cliente.get("/api/practicas").get_json() == [respuesta.get_json()]

def test_portada_entrega_el_formulario_y_los_recursos(cliente):
    respuesta = cliente.get("/")

    assert respuesta.status_code == 200
    assert respuesta.mimetype == "text/html"
    assert b'id="form-practica"' in respuesta.data
    assert b'/js/app.js' in respuesta.data
    assert b'/css/styles.css' in respuesta.data
    assert cliente.get("/js/app.js").status_code == 200
    assert cliente.get("/css/styles.css").status_code == 200


def test_resumen_de_coleccion_vacia_conserva_contrato(cliente):
    practicas.clear()

    resumen = cliente.get("/api/practicas?resumen=true")
    listado = cliente.get("/api/practicas")

    assert resumen.status_code == listado.status_code == 200
    assert resumen.get_json() == {"total": 0, "pendientes": 0, "completadas": 0}
    assert listado.get_json() == []
