"""
Compara el resultado SQL (MAX por año y región) con el calculado en Python.
Agrupa por (Anio, RegionID) para soportar empates de productos.
"""

import pandas as pd
from decimal import Decimal

from practica3.calculo import a_numero


def _preparar_detalle(tabla: pd.DataFrame) -> pd.DataFrame:
    copia = tabla.copy()
    copia["Anio"] = copia["Anio"].astype(int)
    copia["RegionID"] = copia["RegionID"].astype(int)
    copia["Region"] = copia["Region"].astype(str).str.strip()
    copia["Producto"] = copia["Producto"].astype(str).str.strip()
    copia["Ganancia"] = copia["Ganancia"].map(a_numero)
    return copia.sort_values(["Anio", "RegionID", "Producto"]).reset_index(drop=True)


def resumen_por_grupo(tabla: pd.DataFrame) -> pd.DataFrame:
    """Una fila por (Anio, RegionID) con lista ordenada de productos ganadores."""
    filas = []
    for (anio, region_id), grupo in tabla.groupby(["Anio", "RegionID"]):
        productos = sorted(grupo["Producto"].unique())
        filas.append(
            {
                "Anio": int(anio),
                "RegionID": int(region_id),
                "Region": grupo.iloc[0]["Region"],
                "Ganancia": grupo["Ganancia"].max(),
                "Productos": ", ".join(productos),
                "num_productos": len(productos),
            }
        )
    return pd.DataFrame(filas).sort_values(["Anio", "RegionID"]).reset_index(drop=True)


def comparar_sql_vs_python(
    resultado_sql: pd.DataFrame,
    resultado_python: pd.DataFrame,
) -> tuple[bool, pd.DataFrame]:
    sql = resumen_por_grupo(_preparar_detalle(resultado_sql))
    py = resumen_por_grupo(_preparar_detalle(resultado_python))

    comparacion = sql.merge(
        py,
        on=["Anio", "RegionID"],
        how="outer",
        suffixes=("_sql", "_python"),
    )

    cero = Decimal("0")
    ganancia_sql = comparacion["Ganancia_sql"].fillna(cero)
    ganancia_python = comparacion["Ganancia_python"].fillna(cero)

    comparacion["Diff_Ganancia"] = (ganancia_sql - ganancia_python).map(abs)
    comparacion["Coincide_ganancia"] = comparacion["Diff_Ganancia"] == cero
    comparacion["Coincide_productos"] = (
        comparacion["Productos_sql"].fillna("")
        == comparacion["Productos_python"].fillna("")
    )
    comparacion["Coincide"] = (
        comparacion["Coincide_ganancia"] & comparacion["Coincide_productos"]
    )

    esperados = 12  # 3 anios x 4 regiones en Northwind
    todo_ok = bool(
        comparacion["Coincide"].all() and len(comparacion) == esperados
    )

    return todo_ok, comparacion
