"""
Abre la conexión a MySQL y trae los datos como tablas.
"""

import warnings

import mysql.connector
import pandas as pd

from practica4.config import DB_CONFIG
from practica4.consultas import (
    CONSULTA_SQL,
    CONSULTA_PY,
    CONSULTA_RANKING,
    CONSULTA_TOTAL_REGION,
    CONSULTA_TOTAL_VENTAS,
)

warnings.filterwarnings(
    "ignore",
    message="pandas only supports SQLAlchemy connectable.*",
    category=UserWarning,
)


def abrir_conexion():
    return mysql.connector.connect(**DB_CONFIG)


def _leer_sql(conexion, consulta):
    return pd.read_sql(consulta, conexion)


def cargar_datos_desde_mysql():
    conexion = abrir_conexion()

    resultado_sql = _leer_sql(conexion, CONSULTA_SQL)
    ventas_detalle = _leer_sql(conexion, CONSULTA_PY)

    total_region = _leer_sql(conexion, CONSULTA_TOTAL_REGION).iloc[0, 0]
    total_general = _leer_sql(conexion, CONSULTA_TOTAL_VENTAS).iloc[0, 0]

    comparacion_global = {
        "Ventas_total_region": total_region,
        "Ventas_total_general": total_general,
        "Diferencia": total_general - total_region,
        "ranking": _leer_sql(conexion, CONSULTA_RANKING),
    }

    conexion.close()

    return resultado_sql, ventas_detalle, comparacion_global
