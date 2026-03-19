# Demo de Capacidades - Claude Code

Este proyecto demuestra las principales capacidades de Claude Code:

## Lo que se demostró aquí

| Capacidad | Descripción | Archivo |
|-----------|-------------|---------|
| **API REST** | Servidor web completo con FastAPI | `api/main.py` |
| **Procesamiento de datos** | Análisis estadístico y transformaciones | `data/processor.py` |
| **CLI interactivo** | Herramienta de línea de comandos | `cli/tool.py` |
| **Tests automatizados** | Suite completa de pruebas | `tests/` |
| **Generación de datos** | Datos sintéticos para demo | `data/generator.py` |

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### API REST
```bash
uvicorn api.main:app --reload
# Visita http://localhost:8000/docs
```

### CLI
```bash
python cli/tool.py --help
python cli/tool.py stats --records 100
python cli/tool.py analyze --file data/sample.csv
```

### Tests
```bash
pytest tests/ -v
```

## Capacidades demostradas

1. **Generación de código complejo** - APIs, CLIs, procesadores de datos desde cero
2. **Arquitectura limpia** - Código modular, separación de responsabilidades
3. **Testing** - Tests unitarios e integración automáticamente
4. **Documentación** - Código autodocumentado y README
5. **Refactoring** - Mejoras de código existente
6. **Debugging** - Detección y corrección de errores
