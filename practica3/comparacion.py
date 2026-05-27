"""
Compara el resultado que devolvió MySQL con el que calculó Python.
"""

import pandas as pd

from practica3.calculo import a_numero


def _preparar_para_comparar(tabla: pd.DataFrame) -> pd.DataFrame:
    copia = tabla.copy()
    copia["au_id"] = copia["au_id"].astype(str).str.strip()
    copia["Ganancia"] = copia["Ganancia"].map(a_numero).round(2)
    return copia.sort_values("au_id").reset_index(drop=True)


def comparar_sql_vs_python(
    resultado_sql: pd.DataFrame,
    resultado_python: pd.DataFrame,
    tolerancia: float = 0.01,
) -> tuple[bool, pd.DataFrame]:
    """
    Une ambas tablas por au_id y marca si Ganancia coincide.
    """
    sql = _preparar_para_comparar(resultado_sql)
    py = _preparar_para_comparar(resultado_python)

    comparacion = sql.merge(py, on="au_id", how="outer", suffixes=("_sql", "_python"))

    comparacion["Diff_Ganancia"] = (
        comparacion["Ganancia_sql"].fillna(0) - comparacion["Ganancia_python"].fillna(0)
    ).abs()
    comparacion["Coincide"] = comparacion["Diff_Ganancia"] <= tolerancia

    todo_ok = bool(comparacion["Coincide"].all()) and len(comparacion) == len(sql) == len(py)
    return todo_ok, comparacion
