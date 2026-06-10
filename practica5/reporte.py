"""
Imprime en consola los resultados de la validacion de la practica 5.
"""

import pandas as pd

from practica5.comparacion import resumen_clientes_por_grupo, resumen_productos_por_region

REGIONES = {
    1: "Eastern",
    2: "Westerns",
    3: "Northern",
    4: "Southern",
}

_ANCHO = 88


def _separador(titulo: str = "") -> None:
    if titulo:
        print(titulo)
    print("=" * _ANCHO)


def _formatear_moneda(valor) -> str:
    return f"{float(valor):,.2f}"


def _celda_cliente(clientes: str, compras) -> str:
    if not clientes or clientes == "-":
        return "-"
    return f"{clientes} ({_formatear_moneda(compras)})"


def _tabla_productos(resultado: pd.DataFrame) -> pd.DataFrame:
    resumen = resumen_productos_por_region(resultado)
    filas = []
    for region_id, nombre in REGIONES.items():
        match = resumen[resumen["RegionID"] == region_id]
        if match.empty:
            filas.append(
                {
                    "Reg": region_id,
                    "Region": nombre,
                    "Producto": "-",
                    "Ventas": "-",
                }
            )
        else:
            row = match.iloc[0]
            filas.append(
                {
                    "Reg": region_id,
                    "Region": nombre,
                    "Producto": row["Productos"],
                    "Ventas": _formatear_moneda(row["Ventas"]),
                }
            )
    return pd.DataFrame(filas)


def _tabla_clientes_pivote(resultado: pd.DataFrame) -> pd.DataFrame:
    """Una fila por anio, una columna por region (como practica 4)."""
    resumen = resumen_clientes_por_grupo(resultado)
    filas = []

    if resumen.empty:
        return pd.DataFrame(columns=["Anio"] + list(REGIONES.values()))

    for anio in sorted(resumen["Anio"].unique()):
        fila = {"Anio": int(anio)}
        datos_anio = resumen[resumen["Anio"] == anio]
        for region_id, nombre in REGIONES.items():
            match = datos_anio[datos_anio["RegionID"] == region_id]
            if match.empty:
                fila[nombre] = "-"
            else:
                row = match.iloc[0]
                fila[nombre] = _celda_cliente(row["Clientes"], row["Compras"])
        filas.append(fila)

    return pd.DataFrame(filas)


def _tabla_clientes_detalle(resultado: pd.DataFrame) -> pd.DataFrame:
    """Lista compacta: una fila por grupo (anio + region)."""
    resumen = resumen_clientes_por_grupo(resultado)
    if resumen.empty:
        return pd.DataFrame(
            columns=["Anio", "Reg", "Region", "Cliente(s)", "Compras"]
        )

    filas = []
    for _, row in resumen.iterrows():
        filas.append(
            {
                "Anio": int(row["Anio"]),
                "Reg": int(row["RegionID"]),
                "Region": row["Region"],
                "Cliente(s)": row["Clientes"],
                "Compras": _formatear_moneda(row["Compras"]),
            }
        )
    return pd.DataFrame(filas)


def _tabla_comparacion_productos(comparacion: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for _, row in comparacion.iterrows():
        filas.append(
            {
                "Reg": int(row["RegionID"]),
                "Region": row["Region_sql"],
                "Producto": row["Productos_sql"],
                "Ventas SQL": _formatear_moneda(row["Ventas_sql"]),
                "Ventas PY": _formatear_moneda(row["Ventas_python"]),
                "OK": "Si" if row["Coincide"] else "No",
            }
        )
    return pd.DataFrame(filas)


def _tabla_comparacion_clientes(comparacion: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for _, row in comparacion.iterrows():
        filas.append(
            {
                "Anio": int(row["Anio"]),
                "Reg": int(row["RegionID"]),
                "Region": row["Region_sql"],
                "Cliente(s)": row["Clientes_sql"],
                "Compras": _formatear_moneda(row["Compras_sql"]),
                "OK": "Si" if row["Coincide"] else "No",
            }
        )
    return pd.DataFrame(filas)


def _imprimir_df(tabla: pd.DataFrame) -> None:
    with pd.option_context(
        "display.max_columns",
        None,
        "display.width",
        _ANCHO,
        "display.max_colwidth",
        35,
        "display.colheader_justify",
        "left",
    ):
        print(tabla.to_string(index=False))


def _imprimir_pivote(tabla: pd.DataFrame) -> None:
    """Imprime la matriz anio x region con columnas alineadas."""
    columnas = ["Anio"] + list(REGIONES.values())
    filas = tabla.to_dict(orient="records")
    anchos = {col: len(col) for col in columnas}

    for fila in filas:
        for col in columnas:
            texto = str(fila.get(col, "-"))
            anchos[col] = max(anchos[col], len(texto))

    encabezado = "  ".join(col.ljust(anchos[col]) for col in columnas)
    print(encabezado)
    print("  ".join("-" * anchos[col] for col in columnas))
    for fila in filas:
        print("  ".join(str(fila.get(col, "-")).ljust(anchos[col]) for col in columnas))


def _imprimir_evidencias(
    comparacion_productos: pd.DataFrame,
    comparacion_clientes: pd.DataFrame,
    comparacion_global: dict,
    ok_productos: bool,
    ok_clientes: bool,
) -> None:
    total_region = float(
        comparacion_global["Ventas_total_region"]
        if comparacion_global["Ventas_total_region"] is not None
        else 0
    )

    ranking = comparacion_global.get("ranking_productos")
    if ranking is not None and not ranking.empty:
        tops = ranking[ranking["Posicion"] == 1]
        ventas_top = tops["Ventas"].astype(float).sum()
        pct_top = 100 * ventas_top / total_region if total_region else 0
    else:
        ventas_top = 0
        pct_top = 0

    grupos_posibles = 12  # 3 anios x 4 regiones
    grupos_con_dato = len(comparacion_clientes)
    grupos_sin_dato = grupos_posibles - grupos_con_dato

    empates = comparacion_clientes[
        comparacion_clientes["num_clientes_sql"].fillna(1) > 1
    ]

    _separador("8) Evidencias de comprobacion")
    print(f"  Ventas totales:  {_formatear_moneda(total_region)}")
    print(f"  Suma ventas productos top (4 reg): {_formatear_moneda(ventas_top)}")
    print(f"  Productos top / total regional:    {pct_top:.2f}%")
    print()
    print(f"  Productos SQL = Python:  {'SI' if ok_productos else 'NO'} (4/4 regiones)")
    print(
        f"  Clientes SQL = Python:   {'SI' if ok_clientes else 'NO'} "
        f"({grupos_con_dato}/{grupos_con_dato} grupos con datos)"
    )
    print(
        f"  Grupos (anio x region):  {grupos_con_dato} con cliente top, "
        f"{grupos_sin_dato} sin compras del producto top"
    )

    if grupos_sin_dato:
        print()
        print("  Sin cliente top (no hubo ventas del producto top ese anio):")
        presentes = set(
            zip(
                comparacion_clientes["Anio"].astype(int),
                comparacion_clientes["RegionID"].astype(int),
            )
        )
        for anio in sorted({1996, 1997, 1998}):
            faltan = [
                REGIONES[r]
                for r in REGIONES
                if (anio, r) not in presentes
            ]
            if faltan:
                print(f"    {anio}: {', '.join(faltan)}")

    if not empates.empty:
        print()
        print("  Empates (varios clientes con la misma compra maxima):")
        for _, row in empates.iterrows():
            print(
                f"    {int(row['Anio'])} {row['Region_sql']}: "
                f"{row['Clientes_sql']} -> {_formatear_moneda(row['Compras_sql'])}"
            )

    _separador()


def imprimir_resultados(
    top_productos_sql,
    top_productos_python,
    comparacion_productos,
    ok_productos: bool,
    top_clientes_sql,
    top_clientes_python,
    comparacion_clientes,
    ok_clientes: bool,
    comparacion_global,
) -> None:
    validacion_ok = ok_productos and ok_clientes

    print("PRACTICA 5 - Producto top por region y clientes top (Northwind)")
    print("Regiones: 1 Eastern | 2 Westerns | 3 Northern | 4 Southern")
    _separador()

    _separador("1) Producto(s) mas vendidos por region (SQL)")
    _imprimir_df(_tabla_productos(top_productos_sql))

    _separador("2) Cliente(s) top por anio y region - vista pivote (SQL)")
    print("   Formato: Cliente (importe).  '-' = sin ventas del producto top ese anio.")
    _imprimir_pivote(_tabla_clientes_pivote(top_clientes_sql))

    _separador("3) Cliente(s) top - detalle por anio y region (SQL)")
    _imprimir_df(_tabla_clientes_detalle(top_clientes_sql))

    _separador("4) Misma vista pivote calculada en Python")
    _imprimir_pivote(_tabla_clientes_pivote(top_clientes_python))

    _separador("5) Comparacion SQL vs Python - productos (4 regiones)")
    _imprimir_df(_tabla_comparacion_productos(comparacion_productos))

    _separador("6) Comparacion SQL vs Python - clientes (por anio y region)")
    _imprimir_df(_tabla_comparacion_clientes(comparacion_clientes))

    _separador("7) Veredicto")
    if validacion_ok:
        print("  VALIDACION OK: Python reproduce las consultas SQL (incluye empates).")
    else:
        partes = []
        if not ok_productos:
            partes.append("productos")
        if not ok_clientes:
            partes.append("clientes")
        print(f"  VALIDACION FALLIDA: revisa {', '.join(partes)}.")
    _separador()

    _imprimir_evidencias(
        comparacion_productos,
        comparacion_clientes,
        comparacion_global,
        ok_productos,
        ok_clientes,
    )
