"""
Imprime en consola los resultados de la validación de la práctica 4.
"""

import pandas as pd

from practica4.comparacion import resumen_por_grupo

REGIONES = {
    1: "Eastern",
    2: "Westerns",
    3: "Northern",
    4: "Southern",
}

def _tabla_pivote(resultado: pd.DataFrame) -> pd.DataFrame:
    resumen = resumen_por_grupo(resultado)
    filas = []
    for anio in sorted(resumen["Anio"].unique()):
        fila = {"Anio": int(anio)}
        datos_anio = resumen[resumen["Anio"] == anio]
        for region_id, nombre in REGIONES.items():
            match = datos_anio[datos_anio["RegionID"] == region_id]
            if match.empty:
                fila[nombre] = "-"
            else:
                row = match.iloc[0]
                fila[nombre] = f"{row['Productos']} ({float(row['Ganancia']):.4f})"
        filas.append(fila)
    return pd.DataFrame(filas)


def imprimir_resultados(
    resultado_sql,
    resultado_python,
    comparacion,
    validacion_ok: bool,
    comparacion_global,
) -> None:
    cg = comparacion_global

    print("PRACTICA 4 - Mayor ganancia por anio y region (Northwind)")
    print("4 regiones: Eastern | Westerns | Northern | Southern")
    print("================================================================================")

    print("1) Resultado SQL (MySQL: MAX por anio y region)")
    print(_tabla_pivote(resultado_sql).to_string(index=False))
    print("================================================================================")

    print("2) Resultado Python (mismo calculo en codigo)")
    print(_tabla_pivote(resultado_python).to_string(index=False))
    print("================================================================================")

    print("3) Comparacion SQL vs Python (3 anios x 4 regiones = 12 grupos)")
    print(
        comparacion[
            [
                "Anio",
                "RegionID",
                "Region_sql",
                "Productos_sql",
                "Productos_python",
                "Ganancia_sql",
                "Ganancia_python",
                "Coincide",
            ]
        ].to_string(index=False)
    )
    print("================================================================================")

    print("4) Veredicto")
    if validacion_ok:
        print("VALIDACION OK: Python reproduce la consulta SQL (incluye empates).")
    else:
        print("VALIDACION FALLIDA: revisa consultas y calculo en Python.")
    print("================================================================================")

    def _m(valor) -> float:
        return float(valor if valor is not None else 0)

    total_region = _m(cg["Ventas_total_region"])
    total_general = _m(cg["Ventas_total_general"])
    diferencia = _m(cg["Diferencia"])

    print("5) Comparacion global de ventas")
    print(f"   Ventas con region de empleado (CONSULTA_TOTAL_REGION): {total_region:,.2f}")
    print(f"   Ventas totales Northwind (CONSULTA_TOTAL_VENTAS):     {total_general:,.2f}")
    print(f"   Diferencia = total general - con region:                {diferencia:,.2f}")
    print("================================================================================")
