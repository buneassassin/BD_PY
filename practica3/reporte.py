"""
Imprime en consola los resultados de la validación.
"""

from decimal import Decimal

from practica3.comparacion import agregar_fila_auditoria


def imprimir_resultados(
    resultado_sql,
    resultado_python,
    comparacion,
    validacion_ok: bool,
    vista_editorial,
    comparacion_global,
) -> None:
    print("PRACTICA 3 - Ganancias por autor (tienda / Pubs)")
    print("Tablas usadas: titleauthor, titles, sales (solo au_id del autor)")
    print("================================================================================")
    columnas_resumen = ["au_id", "Ganancia"]

    print("1) Resultado SQL (MySQL hace SUM)")
    print(resultado_sql[columnas_resumen].to_string(index=False))
    print("================================================================================")


    print("2) Resultado Python (suma en codigo)")
    print(resultado_python[columnas_resumen].to_string(index=False))
    print("================================================================================")

    print("3) Comparacion SQL vs Python")
    comparacion_con_auditoria = agregar_fila_auditoria(
        comparacion, comparacion_global["suma_desglose"]
    )
    print(
        comparacion_con_auditoria[
            [
                "au_id",
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
    print(f"TOTAL Ganancia_sql:    {total_sql}")
    print(f"TOTAL Ganancia_python: {total_python}")
    print("================================================================================")

    print("4) Veredicto")
    if validacion_ok:
        print("VALIDACION OK: Python reproduce la consulta SQL.")
    else:
        print("VALIDACION FALLIDA: revisa la base de datos y la conexion.")
    
    print("================================================================================")

    print("5) Ventas en sales no reflejadas en el resultado principal")
    if vista_editorial.empty:
        print("   (ninguna)")
    else:
        print(vista_editorial[["title_id", "Ganancia"]].to_string(index=False))
    print("================================================================================")

    def _m(valor) -> float:
        return float(valor)

    cg = comparacion_global
    autores = _m(cg["Ganancia_autores"])
    ventas = _m(cg["Ganancia_ventas_general"])
    diferencia = _m(cg["Diferencia"])
    sin_autor = _m(cg["total_sin_autor"])
    royalty = _m(cg["total_royalty_faltante"])
    suma_desglose = _m(cg["suma_desglose"])

    print("6) Comparacion global")
    print("   Ganancia autores (titleauthor, misma formula del punto 1):")
    print(f"  {autores}")
    print("   Ganancia ventas general (solo sales + titles, al 100%):")
    print(f"  {ventas}")
    print(f"  Diferencia = ventas general - autores = {ventas} - {autores} = {diferencia:.2f}")
    print()
    print("   Desglose de la diferencia:")
    print(f"   a) Ventas sin autor en titleauthor (punto 5): {sin_autor}")
    print("   b) Royalty no repartido al 100% (titulos con autores, pero pct < 100):")
    detalle = cg["royalty_faltante"]
    if detalle.empty:
        print("      (ninguno)")
    else:
        print(
            detalle[
                ["title_id", "venta_bruta", "pct_autores", "pct_editorial", "parte_editorial"]
            ].to_string(index=False)
        )
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f"    Royalty faltante: {royalty}")
    print()
    print(f"   SUMA desglose = {sin_autor} + {royalty} = {suma_desglose}")
    print(f"   (debe coincidir con la diferencia: {diferencia:.2f})")
    print("================================================================================")

