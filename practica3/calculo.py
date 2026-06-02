"""
Cálculo de ganancias en Python (misma lógica que la consulta SQL).

Fórmula por cada venta de un autor en un libro:
    ganancia = cantidad * precio * (royaltyper / 100)
"""

from decimal import Decimal

import pandas as pd


def a_numero(valor) -> Decimal:
    """Convierte valores de MySQL a Decimal (misma precisión que DECIMAL en MySQL)."""
    if valor is None:
        return Decimal("0")
    if isinstance(valor, Decimal):
        return valor
    if isinstance(valor, int):
        return Decimal(valor)
    return Decimal(str(valor))


def ganancia_de_una_venta(cantidad, precio, porcentaje_autor) -> Decimal:
    """
    Una sola línea de venta.
    porcentaje_autor = titleauthor.royaltyper (ej. 50 significa 50 %)
    """
    return (
        a_numero(cantidad)
        * a_numero(precio)
        * a_numero(porcentaje_autor)
        / Decimal("100")
    )


def calcular_ganancias_en_python(ventas_detalle: pd.DataFrame) -> pd.DataFrame:
    """
    Recorre cada fila de ventas_detalle, calcula la ganancia de esa línea
    y luego agrupa por au_id:
      Ganancia = suma de todas sus líneas (como SUM en SQL)
    """

    tabla = ventas_detalle.copy()
    tabla["ganancia_linea"] = tabla.apply(
        lambda fila: ganancia_de_una_venta(
            fila["qty"], fila["price"], fila["royaltyper"]
        ),
        axis=1,
    )

    resumen = []
    for au_id, filas_del_autor in tabla.groupby("au_id"):
        ganancias = filas_del_autor["ganancia_linea"]
        resumen.append(
            {
                "au_id": au_id,
                "Ganancia": sum(ganancias, Decimal("0")),
            }
        )

    return pd.DataFrame(resumen).sort_values("Ganancia", ascending=False)
