"""HU-04: comparación del consumo mensual contra el valor de referencia.

Uso: python src/desviacion.py
"""
import pandas as pd

from db import conectar

# Consumo mensual = suma de los registros del mes, unido con su referencia.
CONSULTA = """
SELECT p.nombre AS proceso,
       m.mes,
       m.consumo_m3,
       r.valor_m3 AS referencia_m3
FROM (
    SELECT proceso_id,
           DATE_FORMAT(fecha, '%Y-%m') AS mes,
           SUM(consumo_m3) AS consumo_m3
    FROM consumos
    GROUP BY proceso_id, mes
) m
JOIN procesos p ON p.id = m.proceso_id
JOIN referencias r ON r.proceso_id = m.proceso_id AND r.mes = m.mes
ORDER BY m.mes, p.nombre
"""


def calcular_desviacion(consumo, referencia):
    """Desviación porcentual con dos decimales: (real - referencia) / referencia * 100."""
    if referencia <= 0:
        raise ValueError("La referencia debe ser mayor que cero")
    return round((consumo - referencia) / referencia * 100, 2)


def obtener_desviaciones():
    """Devuelve un DataFrame con proceso, mes, consumo, referencia y desviación (%)."""
    con = conectar()
    cur = con.cursor()
    cur.execute(CONSULTA)
    filas = cur.fetchall()
    cur.close()
    con.close()
    df = pd.DataFrame(filas, columns=["proceso", "mes", "consumo_m3", "referencia_m3"])
    if df.empty:
        return df.assign(desviacion_pct=pd.Series(dtype=float))
    df["consumo_m3"] = df["consumo_m3"].astype(float)
    df["referencia_m3"] = df["referencia_m3"].astype(float)
    df["desviacion_pct"] = [
        calcular_desviacion(c, r) for c, r in zip(df["consumo_m3"], df["referencia_m3"])
    ]
    return df


if __name__ == "__main__":
    df = obtener_desviaciones()
    if df.empty:
        print("No hay meses con consumo y referencia cargados. Ejecuta sql/referencias.sql.")
    else:
        print(df.to_string(index=False))
