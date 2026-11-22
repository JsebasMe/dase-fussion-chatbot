"""Lógica de conversación (reglas). No usa IA ni servicios externos: no inventa datos."""
import difflib
import re
import unicodedata
from urllib.parse import quote

from .datos import cargar, pesos

D = cargar()
MAX_CHARS = 400
F = "data/negocio.json"

# intención -> palabras clave (sin tildes). Las frases se buscan completas.
CLAVES = {
    "personalizar": ["personalizar", "personalizada", "personalizado", "mi propio", "mi propia",
                     "desde cero", "catalogo", "referencia", "cualquier diseno", "idea"],
    "enviar_diseno": ["enviar diseno", "mandar diseno", "como envio", "formato", "resolucion", "png", "archivo", "foto"],
    "precio": ["precio", "cuanto", "cuesta", "vale", "valor", "cotizar", "cotizacion", "costo", "tarifa"],
    "zonas": ["tamano", "zona", "espalda", "pecho", "manga", "mangas", "grande", "donde"],
    "tallas": ["talla", "tallas", "ninos", "nino", "mujer", "hombre", "xxl"],
    "colores": ["color", "colores", "stock", "disponible", "disponibilidad"],
    "produccion": ["demora", "demoran", "tiempo", "dias", "produccion", "cuando lo tienen", "listo"],
    "envio": ["envio", "envian", "transportadora", "cucuta", "domicilio", "ciudad", "entrega"],
    "cuidados": ["lavar", "lavo", "lavarla", "lavado", "cuidado", "cuidados", "planchar", "secar", "secadora", "suavizante", "dura"],
    "cambios": ["cambio", "devolucion", "devolver", "garantia", "reclamo", "defecto", "reembolso"],
    "composicion": ["tela", "material", "composicion", "algodon", "licra", "poliester"],
    "marcas": ["marca", "marcas", "disney", "derechos", "copyright", "personaje", "personajes"],
    "pago": ["pago", "pagar", "nequi", "transferencia", "efectivo", "tarjeta"],
    "humano": ["whatsapp", "asesor", "persona", "humano", "hablar con", "pedido", "pedir", "comprar", "ordenar"],
    "gracias": ["gracias", "perfecto", "chao", "adios", "hasta luego"],
    "saludo": ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "hey"],
}
NUMEROS = {"un": 1, "una": 1, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6,
           "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "docena": 12}
# Intenciones cuya respuesta termina en una gestión con una persona: muestran el botón de WhatsApp.
CON_WHATSAPP = {"enviar_diseno", "zonas", "colores", "composicion", "marcas", "pago"}
SUGERENCIAS = ["Quiero mi propio diseño", "¿Cuánto cuesta?", "¿Cómo envío mi diseño?", "Cuidados del estampado"]


def normalizar(texto):
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", t)


DEBILES = {"cuanto"}  # palabras que por sí solas no definen la intención (peso 1)


ENVIAR_DISENO = re.compile(r"\b(envi|mand|sub|pas|compart|adjunt|entreg|ma?ndo)\w*(\W+\w+){0,3}?\W+(diseno|logo|foto|imagen|arte|archivo)")


def puntuar(texto):
    """Puntúa cada intención. Cada palabra del cliente suma una sola vez por intención:
    exacta = 2 puntos (1 si es débil), aproximada (error de tipeo) = 1 punto. Acepta plurales."""
    palabras = set(texto.split())
    puntos = {}
    for intencion, claves in CLAVES.items():
        p = sum(2 for c in claves if " " in c and c in texto)
        simples = [c for c in claves if " " not in c]
        for w in palabras:
            forma = w if w in simples else (w[:-1] if w.endswith("s") and w[:-1] in simples else None)
            if forma:
                p += 1 if forma in DEBILES else 2
            elif len(w) >= 5 and difflib.get_close_matches(w, [c for c in simples if len(c) >= 5], n=1, cutoff=0.85):
                p += 1
        if p:
            puntos[intencion] = p
    if ENVIAR_DISENO.search(texto):  # «enviar/mandar/subir mi diseño» siempre es la guía de envío
        puntos["enviar_diseno"] = puntos.get("enviar_diseno", 0) + 5
    return puntos


def extraer_cantidad(texto):
    m = re.search(r"\b(\d{1,3})\b", texto)
    if m:
        return int(m.group(1))
    for palabra in texto.split():
        if palabra in NUMEROS:
            return NUMEROS[palabra]
    return None


def enlace_whatsapp(estado):
    n = estado.get("cantidad")
    detalle = f" Quiero cotizar {n} camisa(s)." if n else ""
    msg = f"Hola DaSe Fussion, vengo del asistente web.{detalle} Quiero estampar mi diseño."
    return f"https://wa.me/{D['whatsapp']}?text={quote(msg)}"


def cotizar(n):
    precios = D["precios"]
    if n < 1:
        return "La cantidad debe ser de al menos 1 camisa. ¿Cuántas quieres?", None
    if str(n) in precios:
        total = precios[str(n)]
        txt = (f"{n} camisa(s) con tu diseño personalizado: {pesos(total)}. Incluye el estampado de hasta "
               f"{D['area']} sin costo adicional. El envío no está incluido y lo paga el cliente.")
        if n == 2:
            txt += f" Equivale a {pesos(total // 2)} cada una."
        return txt, n
    return (f"Para {n} camisas una persona del equipo te cotiza directamente. "
            "Te paso a WhatsApp con tu pedido resumido."), n


def _composicion():
    v = D["composicion_verificada"]
    if v:
        return f"Nuestras camisas son de {D['tela']}. Composición: {v}.", f"{F} › composicion_verificada"
    return (f"Nuestras camisas son de {D['tela']}. Para el detalle exacto de la composición, "
            "una persona te lo confirma por WhatsApp."), f"{F} › tela"


RESPUESTAS = {
    "saludo": lambda: (D["saludo"], f"{F} › saludo"),
    "personalizar": lambda: ("Sí, todo es personalizable. Puedes estampar un nombre, una frase, una foto, un logo o una "
        "ilustración tuya, en el pecho, la espalda, las mangas o varias zonas. Los diseños de referencia que publicamos "
        "son inspiración: no tienes que elegir uno de ellos. Cuéntame qué quieres estampar o pregúntame cómo enviar tu diseño.",
        f"{F} › personalización"),
    "enviar_diseno": lambda: ("¡Perfecto! Para enviarnos tu diseño, escríbenos por WhatsApp con el botón de abajo y "
        "adjunta tu archivo o imagen allí. Lo ideal es un PNG con fondo transparente y buena resolución, pero si solo "
        "tienes una foto, una idea o una referencia, también sirve: cuéntanos qué quieres cambiar. "
        "Antes de estampar te mostramos una vista previa y la apruebas.", f"{F} › politicas"),
    "zonas": lambda: (f"El área total de estampado es de hasta {D['area']}, sin costo adicional. Si pides varias camisas, "
        "todos los diseños deben caber dentro de esa misma área. Para diseños más grandes, una persona te dice qué es posible.",
        f"{F} › area"),
    "tallas": lambda: (D["tallas"], f"{F} › tallas"),
    "colores": lambda: ("Tenemos una amplia variedad de colores. La disponibilidad cambia: pregunta por el stock "
        "del color que quieres por WhatsApp.", f"{F} › colores"),
    "produccion": lambda: (f"La producción toma {D['produccion_dias']} días hábiles, contados desde que se confirma tu pago. "
        "El envío es aparte y depende de la transportadora y la ciudad.", f"{F} › produccion_dias"),
    "envio": lambda: ("Estamos en Cúcuta. El envío lo paga el cliente, tanto en Cúcuta como a otras ciudades de Colombia, "
        "y el tiempo depende de la transportadora.", f"{F} › envío"),
    "cuidados": lambda: ("Para que tu estampado dure: " + " ".join(D["cuidados"]), f"{F} › cuidados"),
    "cambios": lambda: (" ".join(D["politicas"]), f"{F} › politicas"),
    "composicion": _composicion,
    "marcas": lambda: ("Estampamos cualquier diseño. Si incluye marcas registradas o personajes con derechos de autor, "
        "una persona del equipo lo revisa contigo antes de producir.", f"{F} › marcas"),
    "pago": lambda: ("Los medios de pago te los confirma una persona por WhatsApp.", f"{F} › pago"),
    "gracias": lambda: ("¡Con gusto! Si quieres iniciar otra consulta, usa «Nueva conversación».", None),
}
ETIQUETAS = {"personalizar": "personalizar", "enviar_diseno": "enviar mi diseño", "precio": "precios",
             "zonas": "zonas y tamaño", "tallas": "tallas", "colores": "colores", "produccion": "tiempos",
             "envio": "envíos", "cuidados": "cuidados", "cambios": "cambios y garantía", "composicion": "tela",
             "marcas": "marcas y derechos", "pago": "pagos", "humano": "hablar con una persona",
             "gracias": "despedida", "saludo": "saludo"}


AFIRMATIVO = re.compile(r"^(si+|claro|dale|ok|okay|vale|listo|bueno|de una|por favor|porfa|yes)( .*)?$")
ORDINALES = {"1": 0, "primero": 0, "primera": 0, "uno": 0, "el primero": 0, "la primera": 0,
             "2": 1, "segundo": 1, "segunda": 1, "dos": 1, "el segundo": 1, "la segunda": 1}
TRANSITORIAS = ("fallos", "opciones", "ofrecio", "aclarando")  # claves del estado que viven un solo turno


def _limpio(estado):
    return {k: v for k, v in estado.items() if k not in TRANSITORIAS}


def responder(mensaje, estado=None):
    """Recibe el mensaje y el estado de ESTA conversación; devuelve respuesta y nuevo estado.
    El estado recuerda lo último que dijo el bot para no repetirse (evita bucles)."""
    estado = dict(estado or {})
    if not isinstance(mensaje, str) or not mensaje.strip():
        return {"respuesta": "Escribe tu pregunta para que pueda ayudarte. Por ejemplo: «¿cuánto cuesta?»",
                "fuente": None, "estado": estado}
    if len(mensaje) > MAX_CHARS:
        return {"respuesta": f"Tu mensaje es muy largo (máximo {MAX_CHARS} caracteres). "
                             "Resúmelo o envía los detalles por WhatsApp.",
                "fuente": None, "estado": estado, "whatsapp": enlace_whatsapp(estado)}

    texto = normalizar(mensaje).strip()
    texto = re.sub(r" +", " ", texto)

    # 1) El bot ofreció una persona y el cliente acepta («sí», «dale»…)
    if estado.get("ofrecio") == "humano" and AFIRMATIVO.match(texto):
        e = _limpio(estado)
        return {"respuesta": "¡Listo! Un integrante del equipo te atiende por WhatsApp con tu pedido resumido.",
                "fuente": None, "estado": e, "whatsapp": enlace_whatsapp(e)}

    puntos = puntuar(texto)
    cantidad = extraer_cantidad(texto)
    wa, fuente = None, F

    # 2) El bot pidió aclarar entre dos opciones y el cliente elige «1» o «2»
    if estado.get("opciones") and texto in ORDINALES:
        elegida = estado["opciones"][ORDINALES[texto]]
        puntos, cantidad = {elegida: 99}, None
        estado = _limpio(estado)

    # 3) El bot preguntó la cantidad y el cliente responde solo con un número
    if estado.get("esperando") == "cantidad" and cantidad and not puntos:
        resp, n = cotizar(cantidad)
        return {"respuesta": resp, "fuente": f"{F} › precios", "estado": {"cantidad": n, "esperando": None},
                "whatsapp": enlace_whatsapp({"cantidad": n}) if n and n >= 3 else None}

    # 4) Pedido con cantidad sin palabra de precio («quiero 3 camisas»): es una cotización
    if not puntos and cantidad and re.search(r"camisa|camiseta|playera", texto):
        resp, n = cotizar(cantidad)
        return {"respuesta": resp, "fuente": f"{F} › precios", "estado": {"cantidad": n, "esperando": None},
                "whatsapp": enlace_whatsapp({"cantidad": n}) if n and n >= 3 else None}

    # 5) No entendió: la primera vez ofrece ayuda; la segunda seguida pasa directo a una persona
    if not puntos:
        fallos = estado.get("fallos", 0) + 1
        e = {**_limpio(estado), "fallos": fallos, "ofrecio": "humano"}
        if fallos >= 2:
            resp = ("Sigo sin entender bien tu consulta. Mejor te atiende una persona del equipo por WhatsApp: "
                    "toca el botón de abajo.")
        else:
            resp = ("No tengo información sobre eso. Puedo ayudarte con: personalizar tu camisa, precios, cómo enviar "
                    "tu diseño, tallas, tiempos, envíos y cuidados. ¿Quieres que te pase con una persona?")
        return {"respuesta": resp, "fuente": None, "estado": e, "whatsapp": enlace_whatsapp(e)}

    ordenadas = sorted(puntos.items(), key=lambda x: -x[1])
    intencion = ordenadas[0][0]
    if len(ordenadas) > 1 and ordenadas[0][1] == ordenadas[1][1]:
        a, b = ordenadas[0][0], ordenadas[1][0]
        if {a, b} == {"precio", "humano"}:
            intencion = "precio"
        elif "saludo" not in (a, b) and "gracias" not in (a, b) and not estado.get("aclarando"):
            # Primera aclaración. Si ya se aclaró una vez, no se vuelve a preguntar: se responde la primera opción.
            e = {**_limpio(estado), "opciones": [a, b], "aclarando": True}
            return {"respuesta": f"Tu pregunta puede ir por varios lados. ¿Quieres saber sobre «{ETIQUETAS[a]}» "
                                 f"o sobre «{ETIQUETAS[b]}»? (Toca una opción o escribe 1 o 2.)",
                    "fuente": None, "estado": e, "sugerencias": [ETIQUETAS[a], ETIQUETAS[b]]}
    estado = _limpio(estado)  # una respuesta normal borra la memoria de aclaraciones y fallos

    if intencion == "precio":
        if cantidad:
            resp, n = cotizar(cantidad)
            estado = {"cantidad": n, "esperando": None}
            wa = enlace_whatsapp(estado) if n and n >= 3 else None
        else:
            resp = (f"1 camisa: {pesos(D['precios']['1'])}. 2 camisas: {pesos(D['precios']['2'])}. "
                    f"El estampado de hasta {D['area']} no tiene costo adicional. ¿Cuántas camisas necesitas?")
            estado["esperando"] = "cantidad"
        fuente = f"{F} › precios"
    elif intencion == "humano":
        resp, wa = ("Claro. Un integrante del equipo te atiende por WhatsApp con tu pedido ya resumido.",
                    enlace_whatsapp(estado))
    else:
        estado["esperando"] = None
        resp, fuente = RESPUESTAS[intencion]()
        if intencion in CON_WHATSAPP:
            wa = enlace_whatsapp(estado)
    return {"respuesta": resp, "fuente": fuente, "estado": estado, "whatsapp": wa}
