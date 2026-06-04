"""
Texto para explicar el flujo al profesor (python validacion_practicas.py, elige 4).
"""


def mostrar_explicacion() -> None:
    print(
        """
================================================================================
  COMO OBTIENE LOS DATOS PYTHON - PRACTICA 4
================================================================================

  PASO 1 - Conectar a MySQL
  -------------------------
  conexion.py abre la base "tienda".

  PASO 2 - Dos lecturas de las mismas 3 tablas (sales, titles, stores)
  --------------------------------------------------------------------
  A) CONSULTA_SQL: agrupa por año, región y producto; luego MAX(Ganancia)
     por cada par (año, región) y devuelve el producto ganador.

  B) CONSULTA_PY: mismas 3 tablas sin MAX: cada fila es una venta con
     Anio, Region, qty, price, etc.

  PASO 3 - Python (calculo.py)
  ----------------------------
  Por cada fila:  ganancia = qty * price
  Por cada (año, región, producto): Ganancia = suma de líneas
  Por cada (año, región): elige el producto con Ganancia máxima

  PASO 4 - Comparar (comparacion.py)
  ----------------------------------
  Se unen SQL y Python por (Anio, Region). Deben coincidir producto y ganancia.

  Región = stores.state. Año = SUBSTRING(ord_date, 1, 4).

================================================================================
  Archivos
================================================================================
  practica4/consultas.py, calculo.py, comparacion.py, conexion.py, reporte.py
  validacion_practicas.py -> programa principal (elige practica 3 o 4)

"""
    )
