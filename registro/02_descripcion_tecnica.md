# Descripción técnica

## Descripción de funciones (campo máximo 500 caracteres)
Chatbot web en Python para el emprendimiento DaSe Fussion. Explica que se estampa en DTF cualquier diseño del cliente, guía el envío del diseño, cotiza 1 o 2 camisas, informa tallas, tiempos, envíos, políticas y cuidados del estampado con respuestas tomadas de un archivo de datos, reconoce cuándo no tiene información y deriva el pedido resumido a WhatsApp. Sin base de datos ni modelo de IA.

## Descripción ampliada
Núcleo en Python 3 con Flask. Tres capas: interfaz web (`app.py`, `templates/`), lógica de conversación por reglas (`chatbot/logica.py`) y datos (`data/negocio.json`). Ver `docs/03_manual_tecnico.md`.

## Material auxiliar
Código fuente, `docs/03_manual_tecnico.md`, `docs/02_manual_usuario.md`, `docs/informe_pruebas.md`.
