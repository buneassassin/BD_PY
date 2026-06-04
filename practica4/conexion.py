"""
Abre la conexión a MySQL y trae los datos como tablas.
Solo usa las 3 tablas del enunciado: sales, titles, stores.
"""

import mysql.connector
import pandas as pd

from practica4.config import DB_CONFIG
from practica4.consultas import (
    CONSULTA_SQL,
    CONSULTA_PY,
    CONSULTA_TOTAL_AGRUPADO,
    CONSULTA_TOTAL_VENTAS,
    CONSULTA_SIN_TIENDA,
    CONSULTA_RESUMEN_ANIO,
)


def abrir_conexion():
    return mysql.connector.connect(**DB_CONFIG)


def cargar_datos_desde_mysql():
    """
    Devuelve:
      resultado_sql      -> MySQL aplica MAX por año y región
      ventas_detalle     -> cada venta en una fila
      ventas_sin_tienda  -> ventas sin fila en stores (auditoría)
      comparacion_global -> totales globales
    """
    conexion = abrir_conexion()

    resultado_sql = pd.read_sql(CONSULTA_SQL, conexion)
    ventas_detalle = pd.read_sql(CONSULTA_PY, conexion)
    ventas_sin_tienda = pd.read_sql(CONSULTA_SIN_TIENDA, conexion)

    total_agrupado = pd.read_sql(CONSULTA_TOTAL_AGRUPADO, conexion).iloc[0, 0]
    total_ventas = pd.read_sql(CONSULTA_TOTAL_VENTAS, conexion).iloc[0, 0]
    total_sin_tienda = ventas_sin_tienda.iloc[0, 0]
    if total_sin_tienda is None:
        total_sin_tienda = 0
    resumen_anio = pd.read_sql(CONSULTA_RESUMEN_ANIO, conexion)

    comparacion_global = {
        "Ganancia_agrupada": total_agrupado,
        "Ganancia_ventas_general": total_ventas,
        "Diferencia": total_ventas - total_agrupado,
        "total_sin_tienda": total_sin_tienda,
        "resumen_anio": resumen_anio,
        "suma_desglose": total_sin_tienda,
    }

    conexion.close()

    return resultado_sql, ventas_detalle, ventas_sin_tienda, comparacion_global
