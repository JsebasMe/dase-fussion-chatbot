# Manual técnico

## Arquitectura
Tres capas separadas:
| Capa | Archivo | Responsabilidad |
|---|---|---|
| Interfaz | `templates/index.html`, `app.py` | Chat web, rutas `/` y `/chat`, manejo de errores |
| Conversación | `chatbot/logica.py` | Entender la pregunta, contexto, cotizar, enlace de WhatsApp |
| Datos | `chatbot/datos.py`, `data/negocio.json` | Única fuente de precios, plazos, textos |

## Recorrido de un mensaje
1. El navegador envía `POST /chat` con `{mensaje, estado}`.
2. `app.py` valida el cuerpo y llama a `responder(mensaje, estado)`.
3. `responder` revisa si está vacío o excede 400 caracteres.
4. `normalizar` quita tildes y símbolos; `puntuar` suma puntos por intención (palabras clave exactas o con error de tipeo).
5. Si hay contexto (`esperando: cantidad`) y el mensaje es solo un número, cotiza. Si hay empate entre intenciones, pide aclaración. Si no hay coincidencias, reconoce que no sabe y ofrece una persona.
6. La respuesta sale de `negocio.json` y se devuelve con su fuente, el nuevo estado y, si aplica, el enlace de WhatsApp.
7. El navegador pinta el texto con `textContent` (nunca HTML) y guarda el nuevo estado.

## Datos y privacidad
No hay base de datos. El estado de cada conversación (cantidad, si espera un número) vive en el navegador del usuario, por eso no se mezclan conversaciones. El servidor no registra mensajes (`LOG_LEVEL=WARNING`). Conservación: ninguna. Eliminación: «Nueva conversación» o cerrar la pestaña.

## Seguridad
Sin claves ni secretos. Límite de petición de 8 KB. Un error interno devuelve un mensaje genérico, sin detalles. Como no hay modelo generativo, no puede ser manipulado con instrucciones (caso S1).

## Cómo ampliarlo
Nueva respuesta: agregue la intención en `CLAVES`, su texto en `RESPUESTAS` y su nombre en `ETIQUETAS`. Nuevo precio: edite `precios` en `negocio.json` (y `cotizar` si cambia la regla).

## Despliegue
Ver `docs/05_guia_publicacion.md`.
