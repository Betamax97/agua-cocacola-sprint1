# Prototipo de análisis del consumo de agua – Caso Coca-Cola

Prototipo académico (Universidad INCCA de Colombia, Ingeniería de Sistemas, Grupo O) que carga datos simulados de consumo de agua por proceso productivo, los valida y los guarda en MySQL.

**Sprint 1:** repositorio, base de datos y carga de datos (HU-01, HU-02 y HU-03).
**Sprint 2:** rechazo de duplicados (HU-09) y comparación contra valores de referencia (HU-04).

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
2. Crea la base y las tablas. Hay dos formas:

   **Opción A – consola** (necesita que `mysql` esté en el PATH):

   ```bash
   mysql -u root -p < sql/schema.sql
   mysql -u root -p < sql/referencias.sql
   ```

   **Opción B – MySQL Workbench** (recomendada en Windows si la consola dice que `mysql` no se reconoce):

   1. Abre Workbench y conéctate a tu servidor local.
   2. **File → Open SQL Script…** y elige `sql/schema.sql`.
   3. Ejecuta todo el script con el rayo ⚡ (o Ctrl+Shift+Enter).
   4. Repite con `sql/referencias.sql`.
   5. En el panel *Schemas* pulsa actualizar: debe aparecer `agua_cocacola` con las tablas `procesos`, `consumos`, `referencias` y `alertas`.

3. **Solo si ya tenías la base del Sprint 1:** ejecuta también `sql/migracion_sprint2.sql` (borra duplicados y agrega las restricciones únicas). Si creaste la base desde cero en el paso 2, no hace falta.

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

### Regla de duplicados (HU-09)

Un registro es duplicado si ya existe otro con el **mismo proceso y la misma fecha**. La base lo impide con una restricción única (`uq_consumo_proceso_fecha`) y el cargador no lo inserta: al final informa cuántas filas se insertaron y cuántas se omitieron. Por ejemplo, cargar dos veces `consumos_ok.csv` deja 20 registros, no 40.

```bash
python src/cargar_csv.py data/consumos_mixto.csv   # filas nuevas y repetidas: solo entran las nuevas
```

## Comparar contra la referencia (HU-04)

```bash
python src/desviacion.py      # tabla por proceso y mes
python src/grafico.py         # genera salidas/consumo_vs_referencia.png
python src/grafico.py 2026-09 # un mes específico
```

Desviación (%) = (consumo real − referencia) / referencia × 100, con dos decimales. El consumo mensual es la suma de los registros del mes. Los valores de referencia están en `sql/referencias.sql` y son simulados.

## Pruebas

```bash
python -m unittest discover tests -v
```

Validan la fórmula con tres escenarios contra el cálculo manual: leve (tratamiento de residuales, +1,53 %), moderado (refrigeración, +7,13 %) y crítico (lavado de envases, +17,92 %). No necesitan MySQL.

## Estructura

```
src/      código en Python (conexión, carga, desviación y gráfico)
sql/      scripts de la base de datos (esquema, referencias y migración)
data/     archivos CSV de prueba
tests/    pruebas automáticas
docs/     documentación (modelo entidad-relación)
salidas/  gráficos generados (no se suben al repositorio)
```

## Equipo

Jhoan Sebastian Rosas Acero, Fredi Duvan Ramírez Hernández y Hanner Junior Yepez Pacheco.
