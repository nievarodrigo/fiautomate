from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.models.base import Base, engine
from app.api.routes import router
import app.models.cliente  # noqa: F401 - registra modelos en Base
import app.models.fiado    # noqa: F401
import app.models.pago     # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Fiautomate",
    description="Sistema de gestión de fiados con integración MercadoPago y WhatsApp",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
