from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., gt=0)
    categoria: str
    stock: int = Field(..., ge=0)
    creado_en: datetime = Field(default_factory=datetime.now)

    model_config = {"json_schema_extra": {
        "example": {
            "nombre": "Laptop Pro",
            "precio": 1299.99,
            "categoria": "electrónica",
            "stock": 50
        }
    }}


class EstadisticasVenta(BaseModel):
    total_productos: int
    valor_inventario: float
    precio_promedio: float
    precio_max: float
    precio_min: float
    categorias: list[str]


class RespuestaError(BaseModel):
    detalle: str
    codigo: int
