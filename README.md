# Asistente virtual DaSe Fussion · v1.0

Chatbot de reglas en Python (Flask) que explica a los clientes que DaSe Fussion **estampa en DTF cualquier diseño que ellos imaginen**, cotiza 1 o 2 camisas, guía el envío del diseño y deriva el pedido a WhatsApp.

- **Autores:** Juan Sebastián Mendieta Pineda y Danna Nickol Duarte Duarte (Ingeniería Multimedia, 8.º semestre). Docente: Miguel Eduardo Posada Haddad.
- **Versión evaluada:** 1.0
- **Aplicación publicada:** PENDIENTE (ver `docs/05_guia_publicacion.md`)
- **Repositorio:** https://github.com/JsebasMe/dase-fussion-chatbot

## Instalación desde cero
Requisitos: Python 3.10 o superior (probado con 3.12).
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                    # abrir http://localhost:5000
```
No necesita claves ni base de datos. `.env.example` solo lista variables opcionales.

## Cambiar precios, plazos o textos
Edite `data/negocio.json` y reinicie la aplicación. No hay que tocar el código.

## Pruebas
```bash
python -m unittest discover -s tests -t . -v   # pruebas del núcleo
python -m tests.casos                          # 20 casos; genera docs/informe_pruebas.md
```

## Estructura
`app.py` (servidor) · `chatbot/logica.py` (conversación) · `chatbot/datos.py` (datos) · `data/negocio.json` · `templates/index.html` (interfaz) · `docs/` · `registro/` · `tests/`

## Errores frecuentes
| Síntoma | Solución |
|---|---|
| `ModuleNotFoundError: flask` | Active el entorno virtual y ejecute `pip install -r requirements.txt` |
| `Address already in use` | Use otro puerto: `PORT=5001 python app.py` |
| Cambié `negocio.json` y no cambia | Reinicie `python app.py` |
| `JSONDecodeError` al iniciar | Revise comas y comillas en `data/negocio.json` |
"# dase-fussion-chatbot" 
