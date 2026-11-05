"""HU-04: gráfico "Consumo mensual vs referencia" con datos leídos desde MySQL.

Uso: python src/grafico.py            (usa el mes más reciente con referencia)
     python src/grafico.py 2026-09    (un mes específico)
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")  # genera la imagen sin abrir ventana
import matplotlib.pyplot as plt

from desviacion import obtener_desviaciones

SALIDA = os.path.join("salidas", "consumo_vs_referencia.png")


def graficar(mes=None):
    df = obtener_desviaciones()
    if df.empty:
        raise SystemExit("No hay datos con referencia para graficar.")
    mes = mes or df["mes"].max()
    datos = df[df["mes"] == mes]
    if datos.empty:
        raise SystemExit(f"No hay datos con referencia para {mes}.")

    x = range(len(datos))
    ancho = 0.38
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar([i - ancho / 2 for i in x], datos["consumo_m3"], ancho, label="Consumo real", color="#1f6fb2")
    ax.bar([i + ancho / 2 for i in x], datos["referencia_m3"], ancho, label="Referencia", color="#b8c4ce")
    for i, (c, d) in enumerate(zip(datos["consumo_m3"], datos["desviacion_pct"])):
        ax.annotate(f"{d:+.2f} %", (i - ancho / 2, c), ha="center", va="bottom", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels([p.replace("_", "\n") for p in datos["proceso"]], fontsize=9)
    ax.set_ylabel("m³")
    ax.set_title(f"Consumo mensual vs referencia – {mes}")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    os.makedirs("salidas", exist_ok=True)
    fig.savefig(SALIDA, dpi=150)
    print(f"Gráfico guardado en {SALIDA}")


if __name__ == "__main__":
    graficar(sys.argv[1] if len(sys.argv) > 1 else None)
