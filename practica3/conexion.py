"""
Abre la conexión a MySQL y trae los datos como tablas.
Solo usa las 3 tablas del enunciado: titleauthor, titles, sales.
"""

import warnings

import mysql.connector
import pandas as pd

from practica3.config import DB_CONFIG
from practica3.consultas import CONSULTA_SQL, CONSULTA_PY


def abrir_conexion():
    """Crea y devuelve una conexión a la base de datos tienda."""
    return mysql.connector.connect(**DB_CONFIG)


def cargar_datos_desde_mysql():
    """
    Devuelve:
      resultado_sql   -> MySQL calculó SUM (consulta agregada)
      ventas_detalle  -> cada venta en una fila (consulta detalle)
    """
    conexion = abrir_conexion()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            resultado_sql = pd.read_sql(CONSULTA_SQL, conexion)
            ventas_detalle = pd.read_sql(CONSULTA_PY, conexion)
    finally:
        conexion.close()

    return resultado_sql, ventas_detalle
