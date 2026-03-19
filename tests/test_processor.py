"""
Tests unitarios para el procesador de datos.
"""
import csv
import tempfile
import os
import pytest

from data.processor import analizar, formatear_reporte, cargar_csv


@pytest.fixture
def csv_temporal():
    registros = [
        {"id": 1, "producto": "A", "categoria": "tech", "cantidad": 2,
         "precio_unitario": 100.0, "total": 200.0, "fecha": "2024-01-15",
         "region": "Norte", "descuento": 0.0},
        {"id": 2, "producto": "B", "categoria": "ropa", "cantidad": 3,
         "precio_unitario": 50.0, "total": 150.0, "fecha": "2024-02-20",
         "region": "Sur", "descuento": 0.1},
        {"id": 3, "producto": "C", "categoria": "tech", "cantidad": 1,
         "precio_unitario": 500.0, "total": 500.0, "fecha": "2024-01-25",
         "region": "Norte", "descuento": 0.0},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=registros[0].keys())
        writer.writeheader()
        writer.writerows(registros)
        nombre = f.name
    yield nombre
    os.unlink(nombre)


def test_cargar_csv(csv_temporal):
    datos = cargar_csv(csv_temporal)
    assert len(datos) == 3
    assert datos[0]["categoria"] == "tech"


def test_analizar_total_registros(csv_temporal):
    reporte = analizar(csv_temporal)
    assert reporte.total_registros == 3


def test_analizar_ingresos_totales(csv_temporal):
    reporte = analizar(csv_temporal)
    assert reporte.ingresos_totales == pytest.approx(850.0, rel=1e-3)


def test_analizar_categoria_top(csv_temporal):
    reporte = analizar(csv_temporal)
    assert reporte.categoria_top == "tech"


def test_analizar_region_top(csv_temporal):
    reporte = analizar(csv_temporal)
    assert reporte.region_top == "Norte"


def test_analizar_por_categoria_contiene_categorias(csv_temporal):
    reporte = analizar(csv_temporal)
    assert "tech" in reporte.por_categoria
    assert "ropa" in reporte.por_categoria


def test_analizar_tendencia_mensual(csv_temporal):
    reporte = analizar(csv_temporal)
    assert "2024-01" in reporte.tendencia_mensual
    assert "2024-02" in reporte.tendencia_mensual


def test_formatear_reporte_genera_texto(csv_temporal):
    reporte = analizar(csv_temporal)
    texto = formatear_reporte(reporte)
    assert "REPORTE" in texto
    assert "tech" in texto
    assert "Norte" in texto


def test_analizar_archivo_vacio_lanza_error():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        nombre = f.name
    try:
        with pytest.raises(ValueError, match="vacío"):
            analizar(nombre)
    finally:
        os.unlink(nombre)
