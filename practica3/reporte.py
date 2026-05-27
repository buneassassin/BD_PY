"""
Imprime en consola los resultados de la validación.
"""

from practica3.calculo import a_numero


def _titulo(texto: str) -> None:
    print("\n" + "=" * 72)
    print(texto)
    print("=" * 72)


def imprimir_resultados(
    resultado_sql,
    resultado_python,
    comparacion,
    validacion_ok: bool,
) -> None:
    _titulo("PRACTICA 3 - Ganancias por autor (tienda / Pubs)")
    print("Tablas usadas: titleauthor, titles, sales (solo au_id del autor)")

    columnas_resumen = ["au_id", "Ganancia"]

    _titulo("1) Resultado SQL (MySQL hace SUM)")
    print(resultado_sql[columnas_resumen].to_string(index=False))

    _titulo("2) Resultado Python (suma en codigo)")
    print(resultado_python[columnas_resumen].to_string(index=False))

    _titulo("3) Comparacion SQL vs Python")
    print(
        comparacion[
            [
                "au_id",
                "Ganancia_sql",
                "Ganancia_python",
                "Diff_Ganancia",
                "Coincide",
            ]
        ].to_string(index=False)
    )

    _titulo("4) Veredicto")
    if validacion_ok:
        print("VALIDACION OK: Python reproduce la consulta SQL.")
    else:
        print("VALIDACION FALLIDA: revisa la base de datos y la conexion.")

    if not resultado_sql.empty:
        mayor = resultado_sql["Ganancia"].map(a_numero).max()
        top = resultado_sql.iloc[0]
        print(
            f"\nMayor ganancia total: au_id {top['au_id']} -> {mayor:,.2f}"
        )
