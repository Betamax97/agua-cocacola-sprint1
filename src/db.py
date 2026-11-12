import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "agua_cocacola"),
    )


def insertar_consumos(filas):
    """filas: lista de tuplas (proceso, fecha, consumo_m3).

    Devuelve (insertadas, omitidas). Una fila se omite si ya existe un
    registro del mismo proceso en la misma fecha (HU-09).
    """
    con = conectar()
    cur = con.cursor()
    insertadas = 0
    omitidas = 0
    for proceso, fecha, m3 in filas:
        cur.execute("INSERT IGNORE INTO procesos (nombre) VALUES (%s)", (proceso,))
        cur.execute("SELECT id FROM procesos WHERE nombre=%s", (proceso,))
        pid = cur.fetchone()[0]
        cur.execute(
            "INSERT IGNORE INTO consumos (proceso_id, fecha, consumo_m3) VALUES (%s,%s,%s)",
            (pid, fecha, m3),
        )
        if cur.rowcount == 1:
            insertadas += 1
        else:
            omitidas += 1
    con.commit()
    cur.close()
    con.close()
    return insertadas, omitidas


def contar_consumos():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM consumos")
    total = cur.fetchone()[0]
    cur.close()
    con.close()
    return total
