
const API_URL = "/api/practicas";

const formulario = document.getElementById("form-practica");
const lista = document.getElementById("lista-practicas");
const mensaje = document.getElementById("mensaje");

function mostrarMensaje(texto, esError = false) {
    mensaje.textContent = texto;
    mensaje.style.color = esError ? "#b91c1c" : "#166534";
}

async function mensajeDeError(respuesta, estadoEsperado, alternativo) {
    const tipo = respuesta.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase();
    if (respuesta.status !== estadoEsperado || tipo !== "application/json") {
        return alternativo;
    }

    try {
        const datos = await respuesta.json();
        if (typeof datos?.error === "string" && datos.error.trim()) {
            return datos.error.trim();
        }
    } catch {
        return alternativo;
    }

    return alternativo;
}

async function cargarPracticas() {
    const errorConsulta = "No se pudieron consultar las prácticas";
    try {
        const respuesta = await fetch(API_URL);

        if (!respuesta.ok) {
            throw new Error(errorConsulta);
        }

        const practicas = await respuesta.json();
        lista.replaceChildren();

        if (practicas.length === 0) {
            lista.textContent = "Todavía no hay prácticas registradas.";
            return;
        }

        practicas.forEach(practica => {
            const tarjeta = document.createElement("article");
            tarjeta.className = "practica";

            const descripcion = document.createElement("div");

            const titulo = document.createElement("h3");
            titulo.textContent = practica.titulo;

            const curso = document.createElement("p");
            curso.textContent = `Curso: ${practica.curso}`;

            const estado = document.createElement("span");
            estado.textContent = practica.completada
                ? "Completada"
                : "Pendiente";

            descripcion.append(titulo, curso, estado);
            tarjeta.appendChild(descripcion);

            if (!practica.completada) {
                const boton = document.createElement("button");
                boton.textContent = "Completar";

                boton.addEventListener("click", async () => {
                    await completarPractica(practica.id);
                });

                tarjeta.appendChild(boton);
            }

            lista.appendChild(tarjeta);
        });

    } catch {
        lista.textContent = "Error al cargar las prácticas.";
        mostrarMensaje(errorConsulta, true);
    }
}

async function completarPractica(id) {
    const errorFinalizacion = "No se pudo completar la práctica";
    try {
        const respuesta = await fetch(`${API_URL}/${id}`, {
            method: "PATCH"
        });

        if (!respuesta.ok) {
            mostrarMensaje(await mensajeDeError(respuesta, 404, errorFinalizacion), true);
            return;
        }

        mostrarMensaje("Práctica completada correctamente.");
        await cargarPracticas();

    } catch {
        mostrarMensaje(errorFinalizacion, true);
    }
}

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const errorRegistro = "No se pudo registrar la práctica";

    const datos = {
        titulo: document.getElementById("titulo").value.trim(),
        curso: document.getElementById("curso").value.trim()
    };

    try {
        const respuesta = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        });

        if (!respuesta.ok) {
            mostrarMensaje(await mensajeDeError(respuesta, 400, errorRegistro), true);
            return;
        }

        formulario.reset();
        mostrarMensaje("Práctica registrada correctamente.");
        await cargarPracticas();

    } catch {
        mostrarMensaje(errorRegistro, true);
    }
});

cargarPracticas();
