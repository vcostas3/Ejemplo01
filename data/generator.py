"""
Generador de datos sintéticos para demostración.
Demuestra: uso de librerías, generación de datos realistas, exportación CSV.
"""
import random
import csv
from datetime import datetime, timedelta
from pathlib import Path


CATEGORIAS = ["electrónica", "ropa", "hogar", "deportes", "libros", "juguetes", "alimentación"]
ADJETIVOS = ["Pro", "Ultra", "Max", "Plus", "Mini", "Premium", "Lite", "Smart"]
SUSTANTIVOS = ["Dispositivo", "Kit", "Set", "Pack", "Módulo", "Sistema", "Unidad", "Hub"]


def generar_nombre_producto() -> str:
    return f"{random.choice(SUSTANTIVOS)} {random.choice(ADJETIVOS)} {random.randint(100, 999)}"


def generar_fecha_aleatoria(dias_atras: int = 365) -> datetime:
    inicio = datetime.now() - timedelta(days=dias_atras)
    segundos = random.randint(0, int(timedelta(days=dias_atras).total_seconds()))
    return inicio + timedelta(seconds=segundos)


def generar_registro_venta() -> dict:
    cantidad = random.randint(1, 20)
    precio_unitario = round(random.uniform(5.0, 999.99), 2)
    return {
        "id": random.randint(10000, 99999),
        "producto": generar_nombre_producto(),
        "categoria": random.choice(CATEGORIAS),
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "total": round(cantidad * precio_unitario, 2),
        "fecha": generar_fecha_aleatoria().strftime("%Y-%m-%d"),
        "region": random.choice(["Norte", "Sur", "Este", "Oeste", "Centro"]),
        "descuento": round(random.uniform(0, 0.3), 2),
    }


def generar_dataset(n_registros: int = 200, output_path: str = "data/ventas.csv") -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    registros = [generar_registro_venta() for _ in range(n_registros)]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=registros[0].keys())
        writer.writeheader()
        writer.writerows(registros)

    return output_path


if __name__ == "__main__":
    path = generar_dataset(500)
    print(f"Dataset generado: {path}")
