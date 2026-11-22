"""Acceso a datos: lee el archivo propio del negocio (única fuente de las respuestas)."""
import json
from pathlib import Path

RUTA = Path(__file__).resolve().parent.parent / "data" / "negocio.json"


def cargar():
    return json.loads(RUTA.read_text(encoding="utf-8"))


def pesos(valor):
    """50000 -> '$50.000'"""
    return "$" + f"{valor:,}".replace(",", ".")
