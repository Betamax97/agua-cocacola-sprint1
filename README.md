# Prototipo de análisis del consumo de agua – Caso Coca-Cola

Prototipo académico (Universidad INCCA de Colombia, Ingeniería de Sistemas, Grupo O) que carga datos simulados de consumo de agua por proceso productivo, los valida y los guarda en MySQL.

**Sprint 1:** repositorio, base de datos y carga de datos (HU-01, HU-02 y HU-03).

## Requisitos

- Python 3.10 o superior
- MySQL 8 (o compatible) corriendo en tu equipo
- Git

## Instalación

```bash
git clone https://github.com/Betamax97/agua-cocacola-sprint1.git
cd agua-cocacola-sprint1
python -m venv venv
# Windows: venv\Scripts\activate    |    Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

## Configurar la base de datos

1. Copia `.env.example` a `.env` y pon tu usuario y contraseña de MySQL. El archivo `.env` no se sube al repositorio.
2. Crea la base y las tablas:

```bash
mysql -u root -p < sql/schema.sql
```

## Cargar datos

CSV válido:

```bash
python src/cargar_csv.py data/consumos_ok.csv
```

CSV con errores (se rechaza y muestra la fila):

```bash
python src/cargar_csv.py data/consumos_invalido.csv
```

Formato del CSV: columnas `proceso`, `fecha` (AAAA-MM-DD) y `consumo_m3` (número).

## Estructura

```
src/    código en Python (conexión y carga)
sql/    script de la base de datos
data/   archivos CSV de prueba
```

## Equipo

Jhoan Sebastian Rosas Acero, Fredi Duvan Ramírez Hernández y Hanner Junior Yepez Pacheco.
