# Ficha del proyecto

| Campo | Contenido |
|---|---|
| Identificación | Asistente virtual DaSe Fussion, v1.0. Juan Sebastián Mendieta Pineda y Danna Nickol Duarte Duarte |
| Problema | Los clientes creen que solo se estampan los diseños de referencia publicados; no saben que se personaliza cualquier diseño, en cualquier zona |
| Usuarios | Clientes potenciales en Colombia, desde redes sociales, sobre todo en celular |
| Objetivo | Que en menos de un minuto el cliente entienda que puede crear su diseño, sepa cómo enviarlo y cuánto cuesta, y pase a WhatsApp con el pedido resumido |
| Tipo | Chatbot de reglas (sin modelo de IA, sin costo) |
| Conocimiento | `data/negocio.json`, datos entregados por los propietarios del negocio (nov. 2026) |
| Datos y publicación | No se guardan datos del cliente. Alojamiento gratuito. Costo previsto: $0 |

**Incluido:** explicar la personalización, guiar el envío del diseño, cotizar 1 o 2 camisas, tallas, colores (stock por WhatsApp), producción, envío, cuidados, políticas, derivar a una persona.
**Excluido:** cobros, confirmar stock, cotizar 3 o más camisas, recibir archivos, asesoría legal de derechos de autor, guardar datos personales.

## Reglas del negocio
Precio: 1 camisa $50.000; 2 camisas $90.000. Área de estampado hasta 58 x 50 cm sin costo adicional. Producción: 3 días hábiles desde la confirmación del pago. Envío a cargo del cliente. Tela: algodón licrado (sin porcentajes hasta verificar la factura).

## Requisitos y criterios de aceptación
| # | Requisito | Se acepta cuando… | Casos |
|---|---|---|---|
| F1 | Saludo que explica la personalización | El primer mensaje dice que se estampa cualquier diseño y que el catálogo es solo inspiración | A1 |
| F2 | Guía para enviar el diseño | Indica formato, resolución y envío por WhatsApp | A4 |
| F3 | Cotizador | 1 y 2 camisas dan $50.000 y $90.000; desde 3 deriva | A2, A3, C1, C2 |
| F4 | Zonas y tamaño | Informa el límite de 58 x 50 cm | (manual) |
| F5 | Tallas y colores | Muestra tallas y remite el stock a WhatsApp | A5 |
| F6 | Cuidados | Entrega los 5 cuidados verificados | A8 |
| F7 | Producción, envío, políticas | Responde con los datos de la tabla | A6, A7 |
| F8 | Derivación a WhatsApp | Genera enlace con resumen del pedido | A4, C2 |
| F9 | Límites y seguridad | Reconoce lo que no sabe, pide aclaraciones, no obedece instrucciones indebidas | C3, C4, E1–E4, S1–S4 |
