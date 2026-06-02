"""
Abre la conexión a MySQL y trae los datos como tablas.
Solo usa las 3 tablas del enunciado: titleauthor, titles, sales.
"""

import mysql.connector
import pandas as pd

from practica3.config import DB_CONFIG
from practica3.consultas import (
    CONSULTA_SQL,
    CONSULTA_PY,
    CONSULTA_NO_REFLEJADAS,
    CONSULTA_TOTAL_AUTORES,
    CONSULTA_TOTAL_VENTAS,
    CONSULTA_TOTAL_SIN_AUTOR,
    CONSULTA_ROYALTY_FALTANTE,
)


def abrir_conexion():
    """Crea y devuelve una conexión a la base de datos tienda."""
    return mysql.connector.connect(**DB_CONFIG)


def cargar_datos_desde_mysql():
    """
    Devuelve:
      resultado_sql   -> MySQL calculó SUM (consulta agregada)
      ventas_detalle  -> cada venta en una fila (consulta detalle)
      vista_editorial      -> ventas en sales sin fila en titleauthor
      comparacion_global   -> totales globales (autores vs ventas)
    """
    conexion = abrir_conexion()

    resultado_sql = pd.read_sql(CONSULTA_SQL, conexion)
    ventas_detalle = pd.read_sql(CONSULTA_PY, conexion)
    vista_editorial = pd.read_sql(CONSULTA_NO_REFLEJADAS, conexion)

    total_autores = pd.read_sql(CONSULTA_TOTAL_AUTORES, conexion).iloc[0, 0]
    total_ventas = pd.read_sql(CONSULTA_TOTAL_VENTAS, conexion).iloc[0, 0]
    total_sin_autor = pd.read_sql(CONSULTA_TOTAL_SIN_AUTOR, conexion).iloc[0, 0]
    royalty_faltante = pd.read_sql(CONSULTA_ROYALTY_FALTANTE, conexion)
    total_royalty_faltante = royalty_faltante["parte_editorial"].sum()

    comparacion_global = {
        "Ganancia_autores": total_autores,
        "Ganancia_ventas_general": total_ventas,
        "Diferencia": total_ventas - total_autores,
        "total_sin_autor": total_sin_autor,
        "royalty_faltante": royalty_faltante,
        "total_royalty_faltante": total_royalty_faltante,
        "suma_desglose": total_sin_autor + total_royalty_faltante,
    }

    conexion.close()

    return resultado_sql, ventas_detalle, vista_editorial, comparacion_global

