"""
Compara el resultado SQL (MAX por año y región) con el calculado en Python.
"""

import pandas as pd
from decimal import Decimal

from practica3.calculo import a_numero


def _preparar_para_comparar(tabla: pd.DataFrame) -> pd.DataFrame:
    copia = tabla.copy()
    copia["Anio"] = copia["Anio"].astype(str).str.strip()
    copia["Region"] = copia["Region"].astype(str).str.strip()
    copia["Producto"] = copia["Producto"].astype(str).str.strip()
    copia["Ganancia"] = copia["Ganancia"].map(a_numero)
    return copia.sort_values(["Anio", "Region"]).reset_index(drop=True)


def comparar_sql_vs_python(
    resultado_sql: pd.DataFrame,
    resultado_python: pd.DataFrame,
) -> tuple[bool, pd.DataFrame]:
    sql = _preparar_para_comparar(resultado_sql)
    py = _preparar_para_comparar(resultado_python)

    comparacion = sql.merge(
        py,
        on=["Anio", "Region"],
        how="outer",
        suffixes=("_sql", "_python"),
    )

    cero = Decimal("0")
    ganancia_sql = comparacion["Ganancia_sql"].fillna(cero)
    ganancia_python = comparacion["Ganancia_python"].fillna(cero)

    comparacion["Diff_Ganancia"] = (ganancia_sql - ganancia_python).map(abs)
    comparacion["Coincide_ganancia"] = comparacion["Diff_Ganancia"] == cero
    comparacion["Coincide_producto"] = (
        comparacion["Producto_sql"].fillna("")
        == comparacion["Producto_python"].fillna("")
    )
    comparacion["Coincide"] = (
        comparacion["Coincide_ganancia"] & comparacion["Coincide_producto"]
    )

    mismos_grupos = len(comparacion) == len(sql) == len(py)
    todo_ok = bool(comparacion["Coincide"].all() and mismos_grupos)

    return todo_ok, comparacion


def agregar_fila_auditoria(comparacion: pd.DataFrame, ganancia_total) -> pd.DataFrame:
    total = a_numero(ganancia_total)
    fila = pd.DataFrame(
        [
            {
                "Anio": "Total",
                "Region": "",
                "Producto_sql": "",
                "Producto_python": "",
                "Ganancia_sql": total,
                "Ganancia_python": total,
                "Diff_Ganancia": Decimal("0"),
                "Coincide_ganancia": True,
                "Coincide_producto": True,
                "Coincide": True,
            }
        ]
    )
    return pd.concat([comparacion, fila], ignore_index=True)
