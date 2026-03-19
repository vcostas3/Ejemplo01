"""
Tests de integración para la API REST.
Demuestra: pytest, TestClient de FastAPI, fixtures, parametrize.
"""
import pytest
from fastapi.testclient import TestClient

import api.main as main_module
from api.main import app, _db, _poblar_datos_iniciales

client = TestClient(app)


@pytest.fixture(autouse=True)
def restaurar_db():
    """Restaura la base de datos antes de cada test."""
    _db.clear()
    main_module._contador = 0
    _poblar_datos_iniciales()
    yield


class TestRaiz:
    def test_raiz_responde_200(self):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_raiz_contiene_endpoints(self):
        data = resp = client.get("/").json()
        assert "endpoints" in data


class TestListarProductos:
    def test_lista_todos_los_productos(self):
        resp = client.get("/productos")
        assert resp.status_code == 200
        assert len(resp.json()) > 0

    def test_filtrar_por_categoria(self):
        resp = client.get("/productos?categoria=periféricos")
        assert resp.status_code == 200
        for p in resp.json():
            assert p["categoria"] == "periféricos"

    def test_filtrar_por_precio_min(self):
        resp = client.get("/productos?min_precio=100")
        assert resp.status_code == 200
        for p in resp.json():
            assert p["precio"] >= 100

    def test_filtrar_por_precio_max(self):
        resp = client.get("/productos?max_precio=100")
        assert resp.status_code == 200
        for p in resp.json():
            assert p["precio"] <= 100

    def test_filtrar_en_stock(self):
        resp = client.get("/productos?en_stock=true")
        assert resp.status_code == 200
        for p in resp.json():
            assert p["stock"] > 0


class TestObtenerProducto:
    def test_obtener_producto_existente(self):
        resp = client.get("/productos/1")
        assert resp.status_code == 200
        assert resp.json()["id"] == 1

    def test_producto_no_existente_da_404(self):
        resp = client.get("/productos/99999")
        assert resp.status_code == 404

    def test_respuesta_tiene_campos_correctos(self):
        resp = client.get("/productos/1")
        data = resp.json()
        assert all(k in data for k in ["id", "nombre", "precio", "categoria", "stock"])


class TestCrearProducto:
    def test_crear_producto_valido(self):
        nuevo = {"nombre": "Test Product", "precio": 99.99, "categoria": "test", "stock": 10}
        resp = client.post("/productos", json=nuevo)
        assert resp.status_code == 201
        data = resp.json()
        assert data["nombre"] == "Test Product"
        assert data["id"] is not None

    def test_crear_producto_precio_negativo_falla(self):
        nuevo = {"nombre": "Bad Product", "precio": -10, "categoria": "test", "stock": 5}
        resp = client.post("/productos", json=nuevo)
        assert resp.status_code == 422

    def test_crear_producto_nombre_vacio_falla(self):
        nuevo = {"nombre": "", "precio": 10.0, "categoria": "test", "stock": 5}
        resp = client.post("/productos", json=nuevo)
        assert resp.status_code == 422


class TestEliminarProducto:
    def test_eliminar_producto_existente(self):
        resp = client.delete("/productos/1")
        assert resp.status_code == 200
        assert client.get("/productos/1").status_code == 404

    def test_eliminar_producto_inexistente_da_404(self):
        resp = client.delete("/productos/99999")
        assert resp.status_code == 404


class TestEstadisticas:
    def test_estadisticas_retornan_datos(self):
        resp = client.get("/estadisticas")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_productos"] > 0
        assert data["valor_inventario"] > 0
        assert isinstance(data["categorias"], list)


class TestBusqueda:
    def test_busqueda_encuentra_resultados(self):
        resp = client.get("/buscar?q=laptop")
        assert resp.status_code == 200
        assert len(resp.json()) > 0

    def test_busqueda_query_muy_corta_falla(self):
        resp = client.get("/buscar?q=a")
        assert resp.status_code == 422

    def test_busqueda_sin_resultados_retorna_lista_vacia(self):
        resp = client.get("/buscar?q=xyzproducto99999")
        assert resp.status_code == 200
        assert resp.json() == []
