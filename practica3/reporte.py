"""
Imprime en consola los resultados de la validación.
"""

def imprimir_resultados(
    resultado_sql,
    resultado_python,
    comparacion,
    validacion_ok: bool,
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
    print("================================================================================")

    print("4) Veredicto")
    if validacion_ok:
        print("VALIDACION OK: Python reproduce la consulta SQL.")
    else:
        print("VALIDACION FALLIDA: revisa la base de datos y la conexion.")
