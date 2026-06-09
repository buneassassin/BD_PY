"""
Cálculo del producto con mayor ganancia por año y región en Python.

Incluye todos los productos empatados en la ganancia máxima de cada grupo.
"""

from decimal import Decimal

import pandas as pd

from practica3.calculo import a_numero


def ganancia_de_una_venta(cantidad, precio) -> Decimal:
    return a_numero(cantidad) * a_numero(precio)


def calcular_maximos_en_python(ventas_detalle: pd.DataFrame) -> pd.DataFrame:
    """
    Por cada (año, región) devuelve todos los productos cuya ganancia
    coincide con el máximo del grupo (empates incluidos).
    """
    tabla = ventas_detalle.copy()
    tabla["ganancia_linea"] = tabla.apply(
        lambda fila: ganancia_de_una_venta(fila["Quantity"], fila["UnitPrice"]),
        axis=1,
    )

    por_producto = (
        tabla.groupby(["Anio", "RegionID", "Region", "Producto"], as_index=False)
        .agg(Ganancia=("ganancia_linea", lambda xs: sum(xs, Decimal("0"))))
    )

    if por_producto.empty:
        return por_producto

    maximos = []
    for (anio, region_id), filas in por_producto.groupby(["Anio", "RegionID"]):
        ganancia_max = filas["Ganancia"].max()
        ganadores = filas[filas["Ganancia"] == ganancia_max]
        for _, fila in ganadores.iterrows():
            maximos.append(
                {
                    "Anio": anio,
                    "RegionID": region_id,
                    "Region": fila["Region"],
                    "Producto": fila["Producto"],
                    "Ganancia": fila["Ganancia"],
                }
            )

    return (
        pd.DataFrame(maximos)
        .sort_values(["Anio", "RegionID", "Producto"])
        .reset_index(drop=True)
    )
