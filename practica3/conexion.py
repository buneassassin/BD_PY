"""
Abre la conexión a MySQL y trae los datos como tablas.
Solo usa las 3 tablas del enunciado: titleauthor, titles, sales.
"""

import mysql.connector
import pandas as pd

from practica3.config import DB_CONFIG
from practica3.consultas import CONSULTA_SQL, CONSULTA_PY, CONSULTA_EDITORIAL


def abrir_conexion():
    """Crea y devuelve una conexión a la base de datos tienda."""
    return mysql.connector.connect(**DB_CONFIG)


def cargar_datos_desde_mysql():
    """
    Devuelve:
      resultado_sql   -> MySQL calculó SUM (consulta agregada)
      ventas_detalle  -> cada venta en una fila (consulta detalle)
      vista_editorial -> ventas en sales sin fila en titleauthor
    """
    conexion = abrir_conexion()
    
    resultado_sql = pd.read_sql(CONSULTA_SQL, conexion)
    ventas_detalle = pd.read_sql(CONSULTA_PY, conexion)
    vista_editorial = pd.read_sql(CONSULTA_EDITORIAL, conexion)

    conexion.close()

    return resultado_sql, ventas_detalle, vista_editorial

