from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.base import get_db
from app.commands.registry import CommandRegistry
from app.services.fiado_service import FiadoService
from app.webhooks import mercadopago as mp_webhook

router = APIRouter()
command_registry = CommandRegistry()


# ── Webhook WhatsApp (OpenClaw) ────────────────────────────────────────────────

class WhatsAppMessage(BaseModel):
    text: str
    from_number: str = ""


@router.post("/webhook/whatsapp")
async def webhook_whatsapp(msg: WhatsAppMessage, db: Session = Depends(get_db)):
    respuesta = command_registry.dispatch(msg.text, db)
    if respuesta is None:
        return {"reply": None}
    return {"reply": respuesta}


# ── Webhook MercadoPago ────────────────────────────────────────────────────────

@router.post("/webhook/mercadopago")
async def webhook_mercadopago(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    resultado = await mp_webhook.procesar_webhook(payload, db)
    return {"status": resultado}


# ── Dashboard API ──────────────────────────────────────────────────────────────

@router.get("/api/resumen")
def get_resumen(db: Session = Depends(get_db)):
    service = FiadoService(db)
    pendientes = service.fiados.get_pendientes()

    resumen = {}
    for fiado in pendientes:
        nombre = fiado.cliente.nombre
        if nombre not in resumen:
            resumen[nombre] = {"nombre": nombre, "total": 0, "fiados": 0}
        resumen[nombre]["total"] += fiado.monto_pendiente
        resumen[nombre]["fiados"] += 1

    clientes = list(resumen.values())
    total_general = sum(c["total"] for c in clientes)

    return {
        "clientes": sorted(clientes, key=lambda x: x["total"], reverse=True),
        "total_general": total_general,
        "cantidad_clientes": len(clientes),
    }


@router.get("/api/clientes")
def get_clientes(db: Session = Depends(get_db)):
    service = FiadoService(db)
    return [{"id": c.id, "nombre": c.nombre, "telefono": c.telefono} for c in service.clientes.get_all()]


@router.get("/api/clientes/{nombre}")
def get_cliente(nombre: str, db: Session = Depends(get_db)):
    service = FiadoService(db)
    cliente = service.clientes.get_by_nombre(nombre)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    fiados = service.fiados.get_by_cliente(cliente.id)
    return {
        "nombre": cliente.nombre,
        "telefono": cliente.telefono,
        "total_pendiente": sum(f.monto_pendiente for f in fiados if not f.esta_saldado),
        "fiados": [
            {
                "id": f.id,
                "monto_original": f.monto_original,
                "monto_pendiente": f.monto_pendiente,
                "descripcion": f.descripcion,
                "fecha": f.created_at.isoformat(),
                "saldado": f.esta_saldado,
            }
            for f in fiados
        ],
    }
