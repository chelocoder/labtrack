# Entornos de LabTrack

## Desarrollo (DEV)

El desarrollo se realiza localmente en Windows 11,
utilizando Visual Studio Code, Python 3.13 y Flask.

La aplicación se ejecuta mediante:

python -m backend.app

Se accede desde http://127.0.0.1:5000.

El servidor utiliza el modo de depuración de Flask.
Los datos se almacenan temporalmente en memoria.

## Aseguramiento de calidad (QA)

La validación automatizada se realiza mediante pytest.

Las pruebas verifican:
- Disponibilidad del servicio.
- Consulta de prácticas.
- Registro de prácticas.
- Rechazo de registros inválidos.
- Actualización del estado de una práctica.
- Manejo de identificadores inexistentes.

GitHub Actions ejecuta estas pruebas en un runner
Linux con Python 3.13.

Este entorno de validación no constituye un servidor
QA independiente.

## Producción (PROD)

No se ha realizado un despliegue en producción.

Como propuesta para una implementación posterior,
se considera:

- Desactivar el modo de depuración.
- Utilizar un servidor WSGI apropiado.
- Implementar almacenamiento persistente.
- Gestionar las configuraciones mediante variables
  de entorno.
- Restringir los accesos y utilizar HTTPS.

Estas medidas están fuera del alcance funcional
de la versión académica actual.
