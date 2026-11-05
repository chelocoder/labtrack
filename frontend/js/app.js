
const API_URL = "/api/practicas";

const formulario = document.getElementById("form-practica");
const lista = document.getElementById("lista-practicas");
const mensaje = document.getElementById("mensaje");

function mostrarMensaje(texto, esError = false) {
    mensaje.textContent = texto;
    mensaje.style.color = esError ? "#b91c1c" : "#166534";
}

async function cargarPracticas() {
    try {
        const respuesta = await fetch(API_URL);

        if (!respuesta.ok) {
            throw new Error("No se pudieron consultar las prácticas");
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

    } catch (error) {
        lista.textContent = "Error al cargar las prácticas.";
        mostrarMensaje(error.message, true);
    }
}

async function completarPractica(id) {
    try {
        const respuesta = await fetch(`${API_URL}/${id}`, {
            method: "PATCH"
        });

        if (!respuesta.ok) {
            throw new Error("No se pudo completar la práctica");
        }

        mostrarMensaje("Práctica completada correctamente.");
        await cargarPracticas();

    } catch (error) {
        mostrarMensaje(error.message, true);
    }
}

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

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
            throw new Error("No se pudo registrar la práctica");
        }

        formulario.reset();
        mostrarMensaje("Práctica registrada correctamente.");
        await cargarPracticas();

    } catch (error) {
        mostrarMensaje(error.message, true);
    }
});

cargarPracticas();
