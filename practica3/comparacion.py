"""
Compara el resultado que devolvió MySQL con el que calculó Python.

Idea general:
  1) Dejar ambas tablas en el mismo formato (au_id como texto, Ganancia como número).
  2) Poner SQL y Python en una sola tabla, una fila por autor.
  3) Ver si la ganancia de cada autor es igual en ambos lados.
"""

import pandas as pd
from decimal import Decimal

from practica3.calculo import a_numero


def _preparar_para_comparar(tabla: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia una tabla antes de compararla.

    - au_id: texto sin espacios (para que "123" y " 123 " cuenten como el mismo autor).
    - Ganancia: Decimal (mismo tipo que usa MySQL con columnas DECIMAL).
    - Orden por au_id: solo para que las filas salgan siempre en el mismo orden.
    """
    copia = tabla.copy()

    copia["au_id"] = copia["au_id"].astype(str).str.strip()
    copia["Ganancia"] = copia["Ganancia"].map(a_numero)

    copia = copia.sort_values("au_id")
    copia = copia.reset_index(drop=True)
    return copia


def comparar_sql_vs_python(
    resultado_sql: pd.DataFrame,
    resultado_python: pd.DataFrame,
) -> tuple[bool, pd.DataFrame]:
    """
    Devuelve (todo_ok, tabla_comparacion).

    tabla_comparacion tiene por cada au_id:
      Ganancia_sql, Ganancia_python, Diff_Ganancia, Coincide
    """
    sql = _preparar_para_comparar(resultado_sql)
    py = _preparar_para_comparar(resultado_python)

    comparacion = sql.merge(
        py,
        on="au_id",
        how="outer",
        suffixes=("_sql", "_python"),
    )

    cero = Decimal("0")
    ganancia_sql = comparacion["Ganancia_sql"].fillna(cero)
    ganancia_python = comparacion["Ganancia_python"].fillna(cero)

    comparacion["Diff_Ganancia"] = (ganancia_sql - ganancia_python).map(abs)
    comparacion["Coincide"] = comparacion["Diff_Ganancia"] == cero

    mismas_ganancias = comparacion["Coincide"].all()
    mismos_autores = len(comparacion) == len(sql) == len(py)
    todo_ok = bool(mismas_ganancias and mismos_autores)

    return todo_ok, comparacion


def agregar_fila_auditoria(comparacion: pd.DataFrame, ganancia_total) -> pd.DataFrame:
    """Añade la fila Auditoria (diferencia global) al final de la tabla de comparación."""
    total = a_numero(ganancia_total)
    fila = pd.DataFrame(
        [
            {
                "au_id": "Auditoria",
                "Ganancia_sql": total,
                "Ganancia_python": total,
                "Diff_Ganancia": Decimal("0"),
                "Coincide": True,
            }
        ]
    )
    return pd.concat([comparacion, fila], ignore_index=True)
