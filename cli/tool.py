"""
CLI interactivo para análisis de ventas.
Demuestra: typer, rich (tablas, colores, barras de progreso), argumentos tipados.
"""
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import print as rprint
from pathlib import Path
import time

app = typer.Typer(
    name="ventas-cli",
    help="Herramienta CLI para análisis de datos de ventas",
    add_completion=False,
)
console = Console()


@app.command()
def stats(
    records: int = typer.Option(100, "--records", "-n", help="Número de registros a generar"),
    output: str = typer.Option("data/ventas.csv", "--output", "-o", help="Archivo de salida"),
):
    """Genera un dataset sintético y muestra estadísticas."""
    from data.generator import generar_dataset
    from data.processor import analizar, formatear_reporte

    console.rule("[bold blue]Generando Dataset[/bold blue]")

    with console.status(f"[green]Generando {records} registros...[/green]"):
        ruta = generar_dataset(records, output)
        time.sleep(0.5)

    console.print(f"[green]✓[/green] Dataset guardado en [bold]{ruta}[/bold]")

    with console.status("[green]Analizando datos...[/green]"):
        reporte = analizar(ruta)
        time.sleep(0.3)

    # Tabla resumen
    tabla = Table(title="Resumen de Ventas", show_header=True, header_style="bold magenta")
    tabla.add_column("Métrica", style="cyan", width=25)
    tabla.add_column("Valor", justify="right", style="green")

    tabla.add_row("Total registros", f"{reporte.total_registros:,}")
    tabla.add_row("Ingresos totales", f"${reporte.ingresos_totales:,.2f}")
    tabla.add_row("Ingreso promedio", f"${reporte.ingresos_promedio:,.2f}")
    tabla.add_row("Ingreso máximo", f"${reporte.ingresos_max:,.2f}")
    tabla.add_row("Ingreso mínimo", f"${reporte.ingresos_min:,.2f}")
    tabla.add_row("Desviación std", f"${reporte.desviacion_std:,.2f}")
    tabla.add_row("Categoría top", reporte.categoria_top)
    tabla.add_row("Región top", reporte.region_top)

    console.print(tabla)

    # Tabla por categorías
    tabla_cat = Table(title="Por Categoría", header_style="bold yellow")
    tabla_cat.add_column("Categoría", style="cyan")
    tabla_cat.add_column("Ingresos", justify="right", style="green")
    tabla_cat.add_column("Ventas", justify="right")
    tabla_cat.add_column("Unidades", justify="right")

    for cat, res in sorted(reporte.por_categoria.items(), key=lambda x: -x[1].ingresos):
        tabla_cat.add_row(
            cat,
            f"${res.ingresos:,.2f}",
            str(res.total_ventas),
            str(res.unidades),
        )

    console.print(tabla_cat)


@app.command()
def analyze(
    file: str = typer.Argument(..., help="Ruta al archivo CSV de ventas"),
    formato: str = typer.Option("tabla", "--formato", "-f",
                                 help="Formato de salida: tabla | texto"),
):
    """Analiza un archivo CSV de ventas existente."""
    from data.processor import analizar, formatear_reporte

    ruta = Path(file)
    if not ruta.exists():
        console.print(f"[red]Error:[/red] Archivo no encontrado: {file}")
        raise typer.Exit(1)

    with console.status(f"[green]Analizando {ruta.name}...[/green]"):
        reporte = analizar(str(ruta))

    if formato == "texto":
        console.print(formatear_reporte(reporte))
    else:
        panel = Panel(
            f"[bold]Registros:[/bold] {reporte.total_registros:,}\n"
            f"[bold]Ingresos:[/bold] [green]${reporte.ingresos_totales:,.2f}[/green]\n"
            f"[bold]Promedio:[/bold] ${reporte.ingresos_promedio:,.2f}\n"
            f"[bold]Top categoría:[/bold] [yellow]{reporte.categoria_top}[/yellow]\n"
            f"[bold]Top región:[/bold] [yellow]{reporte.region_top}[/yellow]",
            title=f"[bold blue]Análisis: {ruta.name}[/bold blue]",
            border_style="blue",
        )
        console.print(panel)


@app.command()
def demo():
    """Ejecuta una demostración completa de todas las capacidades."""
    rprint("[bold magenta]╔══════════════════════════════════════╗[/bold magenta]")
    rprint("[bold magenta]║     DEMO DE CAPACIDADES - CLAUDE     ║[/bold magenta]")
    rprint("[bold magenta]╚══════════════════════════════════════╝[/bold magenta]")

    capacidades = [
        ("API REST", "FastAPI con CRUD, validación, filtros, docs automáticas"),
        ("Procesamiento de datos", "Análisis estadístico, agrupaciones, tendencias"),
        ("Tests automatizados", "pytest con fixtures, parametrize, integración"),
        ("CLI interactivo", "typer + rich con tablas, colores, progreso"),
        ("Generación de código", "Arquitectura limpia desde cero"),
        ("Documentación", "README, docstrings, esquemas automáticos"),
    ]

    tabla = Table(title="Lo que puede hacer Claude Code", header_style="bold green")
    tabla.add_column("#", style="dim", width=3)
    tabla.add_column("Capacidad", style="cyan bold")
    tabla.add_column("Descripción")

    for i, (cap, desc) in enumerate(capacidades, 1):
        tabla.add_row(str(i), cap, desc)

    console.print(tabla)
    console.print("\n[bold]Ejecuta[/bold] [green]python cli/tool.py stats -n 200[/green] para ver el análisis en acción!")


if __name__ == "__main__":
    app()
