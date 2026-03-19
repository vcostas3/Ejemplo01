"""
Procesador de datos con análisis estadístico.
Demuestra: pandas, numpy, análisis de datos, reportes automáticos.
"""
import csv
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ResumenCategoria:
    categoria: str
    total_ventas: int = 0
    ingresos: float = 0.0
    unidades: int = 0
    precio_promedio: float = 0.0
    regiones: set = field(default_factory=set)


@dataclass
class ReporteAnalisis:
    total_registros: int
    ingresos_totales: float
    ingresos_promedio: float
    ingresos_max: float
    ingresos_min: float
    desviacion_std: float
    categoria_top: str
    region_top: str
    por_categoria: dict[str, ResumenCategoria]
    por_region: dict[str, float]
    tendencia_mensual: dict[str, float]


def cargar_csv(ruta: str) -> list[dict]:
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analizar(ruta: str) -> ReporteAnalisis:
    registros = cargar_csv(ruta)
    if not registros:
        raise ValueError("El archivo CSV está vacío")

    totales = [float(r["total"]) for r in registros]
    por_categoria: dict[str, ResumenCategoria] = defaultdict(lambda: ResumenCategoria(""))
    por_region: dict[str, float] = defaultdict(float)
    por_mes: dict[str, float] = defaultdict(float)

    for r in registros:
        cat = r["categoria"]
        region = r["region"]
        total = float(r["total"])
        mes = r["fecha"][:7]  # YYYY-MM

        resumen = por_categoria[cat]
        resumen.categoria = cat
        resumen.total_ventas += 1
        resumen.ingresos += total
        resumen.unidades += int(r["cantidad"])
        resumen.regiones.add(region)

        por_region[region] += total
        por_mes[mes] += total

    for resumen in por_categoria.values():
        if resumen.total_ventas > 0:
            resumen.precio_promedio = round(resumen.ingresos / resumen.total_ventas, 2)
        resumen.ingresos = round(resumen.ingresos, 2)

    categoria_top = max(por_categoria, key=lambda c: por_categoria[c].ingresos)
    region_top = max(por_region, key=por_region.get)

    return ReporteAnalisis(
        total_registros=len(registros),
        ingresos_totales=round(sum(totales), 2),
        ingresos_promedio=round(statistics.mean(totales), 2),
        ingresos_max=max(totales),
        ingresos_min=min(totales),
        desviacion_std=round(statistics.stdev(totales), 2) if len(totales) > 1 else 0.0,
        categoria_top=categoria_top,
        region_top=region_top,
        por_categoria=dict(por_categoria),
        por_region={k: round(v, 2) for k, v in por_region.items()},
        tendencia_mensual={k: round(v, 2) for k, v in sorted(por_mes.items())},
    )


def formatear_reporte(reporte: ReporteAnalisis) -> str:
    lineas = [
        "=" * 60,
        "  REPORTE DE ANÁLISIS DE VENTAS",
        "=" * 60,
        f"  Total registros:      {reporte.total_registros:,}",
        f"  Ingresos totales:     ${reporte.ingresos_totales:>12,.2f}",
        f"  Ingreso promedio:     ${reporte.ingresos_promedio:>12,.2f}",
        f"  Ingreso máximo:       ${reporte.ingresos_max:>12,.2f}",
        f"  Ingreso mínimo:       ${reporte.ingresos_min:>12,.2f}",
        f"  Desviación estándar:  ${reporte.desviacion_std:>12,.2f}",
        f"  Categoría top:        {reporte.categoria_top}",
        f"  Región top:           {reporte.region_top}",
        "",
        "  POR CATEGORÍA:",
        "-" * 60,
    ]
    for cat, res in sorted(reporte.por_categoria.items(), key=lambda x: -x[1].ingresos):
        lineas.append(f"  {cat:<20} ${res.ingresos:>10,.2f}  ({res.total_ventas} ventas)")

    lineas += ["", "  TENDENCIA MENSUAL:", "-" * 60]
    for mes, total in reporte.tendencia_mensual.items():
        barra = "█" * min(int(total / 500), 30)
        lineas.append(f"  {mes}  {barra} ${total:,.2f}")

    lineas.append("=" * 60)
    return "\n".join(lineas)


if __name__ == "__main__":
    from data.generator import generar_dataset
    ruta = generar_dataset(300)
    reporte = analizar(ruta)
    print(formatear_reporte(reporte))
