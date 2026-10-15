# TP11 – Gestión de Calidad

Proyecto académico de Ingeniería de Software II: análisis de Collatz, regresión de defectos, conversor JSON→CSV y verificación de calidad.

## Instalación (Windows / Git Bash)

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

## Filtro JSON a CSV

```bash
python json2csv.py -i ejemplo.json -o resultado.csv -d ';'
cat ejemplo.json | python json2csv.py > resultado.csv
```

Sin `-i`, toma stdin; sin `-o`, escribe a stdout; delimitador predeterminado: coma. Entrada: objeto JSON plano o lista no vacía de objetos planos. Se arma la unión de columnas en orden de aparición. Los valores anidados se rechazan explícitamente. Ante errores se muestra explicación por stderr y el proceso termina con código 1.

## Validaciones

```bash
python -m pytest tests -v
python -m pytest tests --cov=tp11_calidad --cov-report=term-missing
ruff check .
black --check .
python -m mypy src/tp11_calidad
pyright
bandit -r src/tp11_calidad
pdoc tp11_calidad -o docs/api
```

La cobertura mínima configurada es 85 %. Consultar informe académico adjunto para las sesiones históricas reales de Collatz. Los tests de este repositorio son una implementación nueva y deben validarse en el equipo del estudiante y GitHub Actions.

## Documentación

- `docs/INFORME_TP11.docx`: informe académico entregable, si se copia desde la carpeta de entrega.
- `CONTEXT.md`: prompts utilizados.
- `CHANGELOG.md`: cambios.
- `VERSION` y `BUILD`: información de versión.

## CI

El workflow en `.github/workflows/ci.yml` corre en PR y push. La documentación API se genera en cada ejecución exitosa y se publica como artefacto (no se sobrescribe automáticamente el repositorio del PR).
