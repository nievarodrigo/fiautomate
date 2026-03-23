import hmac
import hashlib
import httpx
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.services.fiado_service import FiadoService


async def verificar_firma(request: Request) -> bool:
    """Verifica la firma del webhook de MercadoPago."""
    if not settings.MP_WEBHOOK_SECRET:
        return True  # En desarrollo, skip verificación

    signature = request.headers.get("x-signature", "")
    data_id = request.headers.get("x-request-id", "")
    body = await request.body()

    manifest = f"id:{data_id};request-id:{data_id};ts:{data_id};"
    expected = hmac.new(
        settings.MP_WEBHOOK_SECRET.encode(),
        manifest.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)


async def obtener_pago_mp(payment_id: str) -> dict | None:
    """Consulta los datos de un pago a la API de MercadoPago."""
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {"Authorization": f"Bearer {settings.MP_ACCESS_TOKEN}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    return None


async def procesar_webhook(payload: dict, db: Session) -> str:
    """
    Procesa la notificación de MercadoPago.
    Busca el pago, extrae descripción y lo cruza con fiados pendientes.
    """
    topic = payload.get("type") or payload.get("topic")
    if topic != "payment":
        return "ignorado"

    payment_id = str(payload.get("data", {}).get("id") or payload.get("id", ""))
    if not payment_id:
        return "sin_id"

    pago_mp = await obtener_pago_mp(payment_id)
    if not pago_mp or pago_mp.get("status") != "approved":
        return "no_aprobado"

    monto = float(pago_mp.get("transaction_amount", 0))
    descripcion = pago_mp.get("description", "") or pago_mp.get("additional_info", {}).get("items", [{}])[0].get("title", "")

    service = FiadoService(db)
    mensaje = service.procesar_pago_mercadopago(payment_id, monto, descripcion)

    return "procesado" if mensaje else "sin_match"
