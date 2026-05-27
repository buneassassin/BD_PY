"""
Texto para explicar el flujo al profesor (python practica3_validacion.py --explicar).
"""


def mostrar_explicacion() -> None:
    print(
        """
================================================================================
  COMO OBTIENE LOS DATOS PYTHON (resumen para explicar al profesor)
================================================================================

  PASO 1 - Conectar a MySQL
  -------------------------
  El modulo conexion.py abre la base de datos "tienda" con mysql.connector.

  PASO 2 - Dos formas de leer los mismos datos
  --------------------------------------------
  A) CONSULTA AGREGADA (consultas.py -> CONSULTA_SQL)
     MySQL une las 3 tablas y ya devuelve Ganancia por autor.
     Eso es lo que validamos como "respuesta correcta del SQL".

  B) CONSULTA DETALLE (consultas.py -> CONSULTA_PY)
     MySQL une las MISMAS 3 tablas pero SIN GROUP BY: cada fila es una venta
     con: au_id, qty, price, royaltyper, etc.
     Python recibe esa "tabla cruda" en memoria (pandas DataFrame).

  PASO 3 - Python calcula solo (calculo.py)
  -----------------------------------------
  Por cada fila:  ganancia = qty * price * royaltyper / 100
  Por cada autor: Ganancia = suma de sus filas

  PASO 4 - Comparar (comparacion.py)
  ----------------------------------
  Se juntan las dos tablas por au_id. Si Ganancia_sql == Ganancia_python
  (con tolerancia 0.01), la practica esta bien hecha.

  NOTA: Solo se usan 3 tablas (titleauthor, titles, sales).
        En pantalla se muestra au_id del autor, sin consultar "authors".

================================================================================
  Archivos del proyecto
================================================================================
  practica3/config.py       -> usuario, clave, base de datos
  practica3/consultas.py    -> texto SQL (2 consultas, 3 tablas)
  practica3/conexion.py     -> leer datos de MySQL
  practica3/calculo.py      -> formula y agrupacion en Python
  practica3/comparacion.py  -> SQL vs Python
  practica3/reporte.py      -> imprimir tablas
  practica3_validacion.py   -> programa principal

"""
    )
