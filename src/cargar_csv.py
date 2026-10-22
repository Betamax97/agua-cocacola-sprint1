import sys
import pandas as pd

COLS = ["proceso", "fecha", "consumo_m3"]


def validar(ruta):
    df = pd.read_csv(ruta)
    faltan = [c for c in COLS if c not in df.columns]
    if faltan:
        raise ValueError(f"Columnas faltantes: {', '.join(faltan)}")
    errores = []
    for i, fila in df.iterrows():
        n = i + 2  # +1 por el encabezado, +1 porque se cuenta desde 1
        if pd.isna(fila["proceso"]) or not str(fila["proceso"]).strip():
            errores.append(f"Fila {n}: proceso vacío")
        if pd.isna(pd.to_datetime(fila["fecha"], errors="coerce")):
            errores.append(f"Fila {n}: fecha inválida ({fila['fecha']})")
        if pd.isna(pd.to_numeric(fila["consumo_m3"], errors="coerce")):
            errores.append(f"Fila {n}: consumo_m3 no numérico ({fila['consumo_m3']})")
    if errores:
        raise ValueError("\n".join(errores))
    return [
        (str(f["proceso"]).strip(), pd.to_datetime(f["fecha"]).date(), float(f["consumo_m3"]))
        for _, f in df.iterrows()
    ]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python src/cargar_csv.py data/consumos_ok.csv")
        sys.exit(1)
    try:
        filas = validar(sys.argv[1])
    except ValueError as e:
        print(f"Archivo rechazado:\n{e}")
        sys.exit(1)
    from db import insertar_consumos, contar_consumos
    insertar_consumos(filas)
    print(f"Se cargaron {len(filas)} registros. Total en base: {contar_consumos()}")
