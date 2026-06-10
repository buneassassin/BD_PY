"""
Compara resultados SQL vs Python para productos top por region
y clientes top por region y anio.
"""

import pandas as pd
from decimal import Decimal

from practica3.calculo import a_numero


def _preparar_productos(tabla: pd.DataFrame) -> pd.DataFrame:
    copia = tabla.copy()
    copia["RegionID"] = copia["RegionID"].astype(int)
    copia["Region"] = copia["Region"].astype(str).str.strip()
    copia["Producto"] = copia["Producto"].astype(str).str.strip()
    copia["Ventas"] = copia["Ventas"].map(a_numero)
    return copia.sort_values(["RegionID", "Producto"]).reset_index(drop=True)


def _preparar_clientes(tabla: pd.DataFrame) -> pd.DataFrame:
    copia = tabla.copy()
    copia["Anio"] = copia["Anio"].astype(int)
    copia["RegionID"] = copia["RegionID"].astype(int)
    copia["Region"] = copia["Region"].astype(str).str.strip()
    copia["Producto"] = copia["Producto"].astype(str).str.strip()
    copia["CustomerID"] = copia["CustomerID"].astype(str).str.strip()
    copia["Cliente"] = copia["Cliente"].astype(str).str.strip()
    copia["Compras"] = copia["Compras"].map(a_numero)
    return copia.sort_values(["Anio", "RegionID", "Cliente"]).reset_index(drop=True)


def resumen_productos_por_region(tabla: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for region_id, grupo in tabla.groupby("RegionID"):
        productos = sorted(grupo["Producto"].unique())
        filas.append(
            {
                "RegionID": int(region_id),
                "Region": grupo.iloc[0]["Region"],
                "Ventas": grupo["Ventas"].max(),
                "Productos": ", ".join(productos),
                "num_productos": len(productos),
            }
        )
    return pd.DataFrame(filas).sort_values("RegionID").reset_index(drop=True)


def resumen_clientes_por_grupo(tabla: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for (anio, region_id), grupo in tabla.groupby(["Anio", "RegionID"]):
        clientes = sorted(grupo["Cliente"].unique())
        filas.append(
            {
                "Anio": int(anio),
                "RegionID": int(region_id),
                "Region": grupo.iloc[0]["Region"],
                "Producto": grupo.iloc[0]["Producto"],
                "Compras": grupo["Compras"].max(),
                "Clientes": ", ".join(clientes),
                "num_clientes": len(clientes),
            }
        )
    return pd.DataFrame(filas).sort_values(["Anio", "RegionID"]).reset_index(drop=True)


def comparar_productos_sql_vs_python(
    resultado_sql: pd.DataFrame,
    resultado_python: pd.DataFrame,
) -> tuple[bool, pd.DataFrame]:
    sql = resumen_productos_por_region(_preparar_productos(resultado_sql))
    py = resumen_productos_por_region(_preparar_productos(resultado_python))

    comparacion = sql.merge(
        py,
        on="RegionID",
        how="outer",
        suffixes=("_sql", "_python"),
    )

    cero = Decimal("0")
    ventas_sql = comparacion["Ventas_sql"].fillna(cero)
    ventas_python = comparacion["Ventas_python"].fillna(cero)

    comparacion["Diff_Ventas"] = (ventas_sql - ventas_python).map(abs)
    comparacion["Coincide_ventas"] = comparacion["Diff_Ventas"] == cero
    comparacion["Coincide_productos"] = (
        comparacion["Productos_sql"].fillna("")
        == comparacion["Productos_python"].fillna("")
    )
    comparacion["Coincide"] = (
        comparacion["Coincide_ventas"] & comparacion["Coincide_productos"]
    )

    esperados = 4
    todo_ok = bool(comparacion["Coincide"].all() and len(comparacion) == esperados)
    return todo_ok, comparacion


def comparar_clientes_sql_vs_python(
    resultado_sql: pd.DataFrame,
    resultado_python: pd.DataFrame,
) -> tuple[bool, pd.DataFrame]:
    sql = resumen_clientes_por_grupo(_preparar_clientes(resultado_sql))
    py = resumen_clientes_por_grupo(_preparar_clientes(resultado_python))

    comparacion = sql.merge(
        py,
        on=["Anio", "RegionID"],
        how="outer",
        suffixes=("_sql", "_python"),
    )

    cero = Decimal("0")
    compras_sql = comparacion["Compras_sql"].fillna(cero)
    compras_python = comparacion["Compras_python"].fillna(cero)

    comparacion["Diff_Compras"] = (compras_sql - compras_python).map(abs)
    comparacion["Coincide_compras"] = comparacion["Diff_Compras"] == cero
    comparacion["Coincide_clientes"] = (
        comparacion["Clientes_sql"].fillna("")
        == comparacion["Clientes_python"].fillna("")
    )
    comparacion["Coincide"] = (
        comparacion["Coincide_compras"] & comparacion["Coincide_clientes"]
    )

    todo_ok = bool(comparacion["Coincide"].all())
    return todo_ok, comparacion
