"""
Imprime en consola los resultados de la validación de la práctica 4.
"""

from decimal import Decimal

from practica4.comparacion import agregar_fila_auditoria


def imprimir_resultados(
    resultado_sql,
    resultado_python,
    comparacion,
    validacion_ok: bool,
    ventas_sin_tienda,
    comparacion_global,
) -> None:
    print("PRACTICA 4 - Producto con mayor ganancia por año y región (Pubs)")
    print("Tablas usadas: sales, titles, stores (región = state de la tienda)")
    print("================================================================================")
    columnas_resumen = ["Anio", "Region", "Producto", "Ganancia"]

    print("1) Resultado SQL (MySQL aplica MAX por año y región)")
    print(resultado_sql[columnas_resumen].to_string(index=False))
    print("================================================================================")

    print("2) Resultado Python (agrupa y elige el máximo por año/región)")
    print(resultado_python[columnas_resumen].to_string(index=False))
    print("================================================================================")

    print("3) Comparacion SQL vs Python")
    comparacion_con_auditoria = agregar_fila_auditoria(
        comparacion, comparacion_global["Ganancia_agrupada"]
    )
    print(
        comparacion_con_auditoria[
            [
                "Anio",
                "Region",
                "Producto_sql",
                "Producto_python",
                "Ganancia_sql",
                "Ganancia_python",
                "Diff_Ganancia",
                "Coincide",
            ]
        ].to_string(index=False)
    )
    print("================================================================================")
    cero = Decimal("0")
    total_sql = comparacion["Ganancia_sql"].fillna(cero).sum()
    total_python = comparacion["Ganancia_python"].fillna(cero).sum()
    print(f"TOTAL Ganancia_sql (solo ganadores):    {total_sql}")
    print(f"TOTAL Ganancia_python (solo ganadores): {total_python}")
    print("================================================================================")

    print("4) Veredicto")
    if validacion_ok:
        print("VALIDACION OK: Python reproduce la consulta SQL.")
    else:
        print("VALIDACION FALLIDA: revisa la base de datos y la conexion.")
    print("================================================================================")

    print("5) Ventas en sales sin tienda en stores")
    total_sin = ventas_sin_tienda.iloc[0, 0]
    if total_sin in (None, 0, Decimal("0")):
        print("   (ninguna)")
    else:
        print(f"   total_sin_tienda = {total_sin}")
    print("================================================================================")

    def _m(valor) -> float:
        return float(valor if valor is not None else 0)

    cg = comparacion_global
    agrupada = _m(cg["Ganancia_agrupada"])
    ventas = _m(cg["Ganancia_ventas_general"])
    diferencia = _m(cg["Diferencia"])
    sin_tienda = _m(cg["total_sin_tienda"])
    suma_desglose = _m(cg["suma_desglose"])

    print("6) Comparacion global")
    print("   Ganancia agrupada (sales + titles + stores, todos los productos):")
    print(f"  {agrupada}")
    print("   Ganancia ventas general (solo sales + titles, al 100%):")
    print(f"  {ventas}")
    print(f"  Diferencia = ventas general - agrupada = {ventas} - {agrupada} = {diferencia:.2f}")
    print()
    print("   Desglose de la diferencia:")
    print(f"   a) Ventas sin tienda en stores: {sin_tienda}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f"   SUMA desglose = {sin_tienda} = {suma_desglose}")
    print(f"   (debe coincidir con la diferencia: {diferencia:.2f})")
    print()
    print("   Totales por año (auditoría):")
    print(cg["resumen_anio"].to_string(index=False))
    print("================================================================================")
