# Guía de publicación (PythonAnywhere, plan gratuito)

**Estado: NO publicado.** Esta guía no se ha ejecutado todavía.

## Costos y límites (consultados el 21/11/2026; verifique antes de publicar)
Costo: $0. El plan gratuito de PythonAnywhere permite 1 aplicación web, 100 segundos de CPU, 512 MiB de disco y vence al mes (hay que renovarla con un clic). Las llamadas a internet desde el servidor están limitadas; este bot no hace ninguna. Responsable de la cuenta: PENDIENTE (nombre).

## Pasos
1. Cree una cuenta gratuita en pythonanywhere.com.
2. En **Files**, suba `DaSe_Fussion_Chatbot_*.zip` y descomprímalo en una consola: `unzip archivo.zip`.
3. En una consola Bash: `cd dase-fussion-chatbot && python3 -m venv ~/venv && source ~/venv/bin/activate && pip install -r requirements.txt`.
4. En **Web → Add a new web app → Manual configuration** (misma versión de Python del entorno).
5. En *Virtualenv* escriba `/home/SU_USUARIO/venv`.
6. Edite el archivo WSGI y deje solo:
```python
import sys
ruta = "/home/SU_USUARIO/dase-fussion-chatbot"
if ruta not in sys.path:
    sys.path.insert(0, ruta)
from app import app as application
```
7. Pulse **Reload** y abra `https://SU_USUARIO.pythonanywhere.com`.

## Variables de entorno
Ninguna obligatoria (no hay claves).

## Comprobaciones desde otro dispositivo (PENDIENTES)
- [ ] El enlace abre en un celular con datos móviles
- [ ] El saludo aparece y una pregunta recibe respuesta
- [ ] El botón de WhatsApp abre el chat correcto
- [ ] Anotar fecha de la comprobación y dispositivo: ________
- [ ] Renovar el vencimiento mensual antes de la sustentación
