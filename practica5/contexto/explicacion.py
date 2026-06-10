"""
Texto para explicar el flujo al profesor (python validacion_practicas.py, elige 5).
"""


def mostrar_explicacion() -> None:
    print(
        """
================================================================================
  PRACTICA 5 - FLUJO
================================================================================

  Paso 1: producto(s) con MAYOR venta en cada region (4 regiones).
  Paso 2: cliente(s) que mas compraron ESE producto, por region y anio.

  Consultas en consultas.py:
    CONSULTA_TOP_PRODUCTOS_SQL, CONSULTA_TOP_CLIENTES_SQL, CONSULTA_PY,
    CONSULTA_TOTAL_REGION, CONSULTA_RANKING_PRODUCTOS, CONSULTA_RANKING_CLIENTES

  Regiones (tabla region):
    1 Eastern | 2 Westerns | 3 Northern | 4 Southern

  Venta linea = Quantity * UnitPrice
  Region via empleado del pedido (employeeterritories -> territories -> region)

  Empates: si dos productos o clientes empatan en el maximo del grupo,
  se muestran juntos en el reporte.

  SQL standalone en sql/practica5_top_producto_region.sql y
  sql/practica5_top_clientes_region_anio.sql

================================================================================
"""
    )
