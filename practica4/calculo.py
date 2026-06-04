"""
Cálculo de ganancias y máximo por año/región en Python.

Fórmula por cada venta:
    ganancia = cantidad * precio
"""

from decimal import Decimal

import pandas as pd

from practica3.calculo import a_numero


def ganancia_de_una_venta(cantidad, precio) -> Decimal:
    return a_numero(cantidad) * a_numero(precio)


def _agrupar_por_producto(ventas_detalle: pd.DataFrame) -> pd.DataFrame:
    tabla = ventas_detalle.copy()
    tabla["ganancia_linea"] = tabla.apply(
        lambda fila: ganancia_de_una_venta(fila["qty"], fila["price"]),
        axis=1,
    )

    resumen = []
    for claves, filas in tabla.groupby(["Anio", "Region", "Producto"]):
        anio, region, producto = claves
        ganancias = filas["ganancia_linea"]
        resumen.append(
            {
                "Anio": anio,
                "Region": region,
                "Producto": producto,
                "Ganancia": sum(ganancias, Decimal("0")),
            }
        )

    return pd.DataFrame(resumen)


def calcular_maximos_en_python(ventas_detalle: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa por año, región y producto; luego conserva el producto
    con mayor ganancia en cada par (Anio, Region).
    """
    por_producto = _agrupar_por_producto(ventas_detalle)
    if por_producto.empty:
        return por_producto

    maximos = []
    for (anio, region), filas in por_producto.groupby(["Anio", "Region"]):
        mejor = filas.loc[filas["Ganancia"].idxmax()]
        maximos.append(
            {
                "Anio": anio,
                "Region": region,
                "Producto": mejor["Producto"],
                "Ganancia": mejor["Ganancia"],
            }
        )

    return (
        pd.DataFrame(maximos)
        .sort_values(["Anio", "Region"])
        .reset_index(drop=True)
    )
