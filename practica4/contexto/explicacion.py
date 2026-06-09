"""
Texto para explicar el flujo al profesor (python validacion_practicas.py, elige 4).
"""


def mostrar_explicacion() -> None:
    print(
        """
================================================================================
  PRACTICA 4 - FLUJO
================================================================================

  SQL (ProductosMenosVendidos.sql)     -> MIN, solo SQL, pivote con empates
  Python (validacion_practicas.py 4)   -> MAX, SQL + Python, misma estructura

  Consultas en consultas.py (como practica 3):
    CONSULTA_SQL, CONSULTA_PY,
    CONSULTA_TOTAL_REGION, CONSULTA_TOTAL_VENTAS

  Regiones (tabla region):
    1 Eastern | 2 Westerns | 3 Northern | 4 Southern

  Ganancia linea = Quantity * UnitPrice

  Empates: si dos productos tienen la misma ganancia extrema en un anio/region,
  se muestran juntos:  "Producto A, Producto B (123.4500)"

  Control de ventas en el reporte:
    - Total general Northwind
    - Total con region de empleado (base del ejercicio)
    - Ventas por anio
    - Ventas por anio y region (matriz 3 x 4)

================================================================================
"""
    )
