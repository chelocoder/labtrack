# LabTrack

Aplicación web para registrar y realizar el seguimiento
de prácticas de aprendizaje en formación técnica.

## Contexto

Proyecto académico del curso Ingeniería de Software II.

Caso de aplicación: seguimiento de prácticas en un centro de formación técnica.

## Funcionalidades implementadas

1. Registrar prácticas de aprendizaje.
2. Consultar las prácticas registradas.
3. Marcar prácticas como completadas.

## Tecnologías

- Python y Flask
- HTML, CSS y JavaScript
- Git y GitHub
- GitHub Actions
- pytest

## Estado

Proyecto en fase de revisión.


## Instalación

### Requisitos

- Python 3.13
- Git
- pip

### Clonar el repositorio

```bash
git clone https://github.com/chelocoder/labtrack.git
cd labtrack
git switch develop
```

### Crear el entorno virtual

```bash
python -m venv .venv
```

Activarlo desde Git Bash en Windows:

```bash
source .venv/Scripts/activate
```

### Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

## Ejecución local

Iniciar el servidor Flask:

```bash
python -m backend.app
```

Abrir en el navegador:

http://127.0.0.1:5000

La aplicación permite registrar, consultar y completar
prácticas de aprendizaje desde la interfaz web.

## Pruebas automatizadas

Ejecutar:

```bash
python -m pytest -v
```

La batería actual comprende seis pruebas automatizadas.

## Control de versiones

- `main`: rama principal.
- `develop`: integración de funcionalidades.
- `feature/*`: desarrollo de cambios independientes.

La integración se realiza mediante pull requests.

## Integración continua

El archivo `.github/workflows/ci.yml` define un
pipeline de GitHub Actions que instala las dependencias
y ejecuta pytest cuando se realizan cambios o se proponen
pull requests hacia `develop` y `main`.

## Documentación técnica

- `docs/casos-uso.puml`: diagrama de casos de uso.
- `docs/componentes.puml`: diagrama de componentes.
- `docs/despliegue.puml`: diagrama de despliegue.
- `docs/entornos.md`: descripción de DEV, QA y PROD.

## Limitaciones

Los registros se almacenan en memoria y se pierden
cuando el servidor Flask se reinicia.

La versión actual está destinada a demostración y
evaluación académica. No se ha desplegado en producción.
```
