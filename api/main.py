"""
API REST completa para gestión de inventario.
Demuestra: routing, validación, manejo de errores, documentación automática.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime

from api.models import Producto, EstadisticasVenta

app = FastAPI(
    title="Demo Inventario API",
    description="API de ejemplo que demuestra capacidades de Claude Code",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos en memoria para demo
_db: dict[int, Producto] = {}
_contador = 0


def _siguiente_id() -> int:
    global _contador
    _contador += 1
    return _contador


def _poblar_datos_iniciales():
    productos_iniciales = [
        Producto(nombre="Laptop Pro 15", precio=1299.99, categoria="electrónica", stock=25),
        Producto(nombre="Mouse Inalámbrico", precio=45.99, categoria="periféricos", stock=150),
        Producto(nombre="Teclado Mecánico", precio=89.99, categoria="periféricos", stock=80),
        Producto(nombre="Monitor 4K 27\"", precio=599.99, categoria="electrónica", stock=40),
        Producto(nombre="Auriculares BT", precio=199.99, categoria="audio", stock=60),
        Producto(nombre="Webcam HD", precio=79.99, categoria="periféricos", stock=95),
        Producto(nombre="SSD 1TB", precio=119.99, categoria="almacenamiento", stock=200),
        Producto(nombre="Hub USB-C", precio=49.99, categoria="accesorios", stock=120),
    ]
    for p in productos_iniciales:
        pid = _siguiente_id()
        p.id = pid
        _db[pid] = p


_poblar_datos_iniciales()


@app.get("/", summary="Bienvenida")
def raiz():
    return {
        "mensaje": "API de Inventario - Demo Claude Code",
        "docs": "/docs",
        "endpoints": ["/productos", "/productos/{id}", "/estadisticas", "/buscar"],
    }


@app.get("/productos", response_model=list[Producto], summary="Listar productos")
def listar_productos(
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    min_precio: Optional[float] = Query(None, ge=0),
    max_precio: Optional[float] = Query(None, ge=0),
    en_stock: bool = Query(False, description="Solo productos con stock > 0"),
):
    productos = list(_db.values())

    if categoria:
        productos = [p for p in productos if p.categoria.lower() == categoria.lower()]
    if min_precio is not None:
        productos = [p for p in productos if p.precio >= min_precio]
    if max_precio is not None:
        productos = [p for p in productos if p.precio <= max_precio]
    if en_stock:
        productos = [p for p in productos if p.stock > 0]

    return productos


@app.get("/productos/{producto_id}", response_model=Producto, summary="Obtener producto")
def obtener_producto(producto_id: int):
    if producto_id not in _db:
        raise HTTPException(status_code=404, detail=f"Producto {producto_id} no encontrado")
    return _db[producto_id]


@app.post("/productos", response_model=Producto, status_code=201, summary="Crear producto")
def crear_producto(producto: Producto):
    pid = _siguiente_id()
    producto.id = pid
    producto.creado_en = datetime.now()
    _db[pid] = producto
    return producto


@app.put("/productos/{producto_id}", response_model=Producto, summary="Actualizar producto")
def actualizar_producto(producto_id: int, datos: Producto):
    if producto_id not in _db:
        raise HTTPException(status_code=404, detail=f"Producto {producto_id} no encontrado")
    datos.id = producto_id
    datos.creado_en = _db[producto_id].creado_en
    _db[producto_id] = datos
    return datos


@app.delete("/productos/{producto_id}", summary="Eliminar producto")
def eliminar_producto(producto_id: int):
    if producto_id not in _db:
        raise HTTPException(status_code=404, detail=f"Producto {producto_id} no encontrado")
    del _db[producto_id]
    return {"mensaje": f"Producto {producto_id} eliminado correctamente"}


@app.get("/estadisticas", response_model=EstadisticasVenta, summary="Estadísticas del inventario")
def estadisticas():
    if not _db:
        raise HTTPException(status_code=404, detail="No hay productos en el inventario")

    productos = list(_db.values())
    precios = [p.precio for p in productos]
    return EstadisticasVenta(
        total_productos=len(productos),
        valor_inventario=sum(p.precio * p.stock for p in productos),
        precio_promedio=round(sum(precios) / len(precios), 2),
        precio_max=max(precios),
        precio_min=min(precios),
        categorias=sorted(set(p.categoria for p in productos)),
    )


@app.get("/buscar", response_model=list[Producto], summary="Búsqueda de productos")
def buscar(q: str = Query(..., min_length=2, description="Término de búsqueda")):
    q_lower = q.lower()
    resultados = [
        p for p in _db.values()
        if q_lower in p.nombre.lower() or q_lower in p.categoria.lower()
    ]
    return resultados
