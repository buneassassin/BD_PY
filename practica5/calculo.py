"""
Calculo en Python del producto top por region y clientes top por region y anio.

Incluye empates en productos y clientes con el mismo valor maximo del grupo.
"""

from decimal import Decimal

import pandas as pd

from practica3.calculo import a_numero


def venta_de_una_linea(cantidad, precio) -> Decimal:
    return a_numero(cantidad) * a_numero(precio)


def _agregar_ventas(tabla: pd.DataFrame) -> pd.DataFrame:
    copia = tabla.copy()
    copia["venta_linea"] = copia.apply(
        lambda fila: venta_de_una_linea(fila["Quantity"], fila["UnitPrice"]),
        axis=1,
    )
    return copia


def calcular_top_productos_en_python(ventas_detalle: pd.DataFrame) -> pd.DataFrame:
    """Producto(s) con mayor venta en cada region."""
    tabla = _agregar_ventas(ventas_detalle)

    por_producto = (
        tabla.groupby(["RegionID", "Region", "Producto"], as_index=False)
        .agg(Ventas=("venta_linea", lambda xs: sum(xs, Decimal("0"))))
    )

    if por_producto.empty:
        return por_producto

    ganadores = []
    for region_id, filas in por_producto.groupby("RegionID"):
        venta_max = filas["Ventas"].max()
        tops = filas[filas["Ventas"] == venta_max]
        for _, fila in tops.iterrows():
            ganadores.append(
                {
                    "RegionID": int(region_id),
                    "Region": fila["Region"],
                    "Producto": fila["Producto"],
                    "Ventas": fila["Ventas"],
                }
            )

    return (
        pd.DataFrame(ganadores)
        .sort_values(["RegionID", "Producto"])
        .reset_index(drop=True)
    )


def calcular_top_clientes_en_python(
    ventas_detalle: pd.DataFrame,
    top_productos: pd.DataFrame,
) -> pd.DataFrame:
    """Cliente(s) que mas compraron los productos top, por region y anio."""
    if top_productos.empty:
        return pd.DataFrame()

    productos_top = set(
        zip(top_productos["RegionID"].astype(int), top_productos["Producto"].astype(str).str.strip())
    )

    tabla = _agregar_ventas(ventas_detalle)
    tabla["RegionID"] = tabla["RegionID"].astype(int)
    tabla["Producto"] = tabla["Producto"].astype(str).str.strip()
    tabla["Cliente"] = tabla["Cliente"].astype(str).str.strip()
    tabla = tabla[
        tabla.apply(
            lambda fila: (fila["RegionID"], fila["Producto"]) in productos_top,
            axis=1,
        )
    ]

    if tabla.empty:
        return pd.DataFrame()

    por_cliente = (
        tabla.groupby(
            ["Anio", "RegionID", "Region", "Producto", "CustomerID", "Cliente"],
            as_index=False,
        )
        .agg(Compras=("venta_linea", lambda xs: sum(xs, Decimal("0"))))
    )

    ganadores = []
    for (anio, region_id), filas in por_cliente.groupby(["Anio", "RegionID"]):
        compra_max = filas["Compras"].max()
        tops = filas[filas["Compras"] == compra_max]
        for _, fila in tops.iterrows():
            ganadores.append(
                {
                    "Anio": int(anio),
                    "RegionID": int(region_id),
                    "Region": fila["Region"],
                    "Producto": fila["Producto"],
                    "CustomerID": fila["CustomerID"],
                    "Cliente": fila["Cliente"],
                    "Compras": fila["Compras"],
                }
            )

    return (
        pd.DataFrame(ganadores)
        .sort_values(["Anio", "RegionID", "Cliente"])
        .reset_index(drop=True)
    )
