"""
Abre la conexion a MySQL y trae los datos como tablas.
"""

import warnings

import mysql.connector
import pandas as pd

from practica5.config import DB_CONFIG
from practica5.consultas import (
    CONSULTA_PY,
    CONSULTA_RANKING_CLIENTES,
    CONSULTA_RANKING_PRODUCTOS,
    CONSULTA_TOP_CLIENTES_SQL,
    CONSULTA_TOP_PRODUCTOS_SQL,
    CONSULTA_TOTAL_REGION,
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

    top_productos_sql = _leer_sql(conexion, CONSULTA_TOP_PRODUCTOS_SQL)
    top_clientes_sql = _leer_sql(conexion, CONSULTA_TOP_CLIENTES_SQL)
    ventas_detalle = _leer_sql(conexion, CONSULTA_PY)

    total_region = _leer_sql(conexion, CONSULTA_TOTAL_REGION).iloc[0, 0]

    comparacion_global = {
        "Ventas_total_region": total_region,
        "ranking_productos": _leer_sql(conexion, CONSULTA_RANKING_PRODUCTOS),
        "ranking_clientes": _leer_sql(conexion, CONSULTA_RANKING_CLIENTES),
    }

    conexion.close()

    return top_productos_sql, top_clientes_sql, ventas_detalle, comparacion_global
