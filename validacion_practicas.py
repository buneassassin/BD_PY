"""
Validación SQL vs Python.

Ejecutar:  python validacion_practicas.py
El programa pregunta qué práctica quieres correr.
"""


def practica3():
    from practica3.conexion import cargar_datos_desde_mysql
    from practica3.calculo import calcular_ganancias_en_python
    from practica3.comparacion import comparar_sql_vs_python
    from practica3.reporte import imprimir_resultados

    sql, detalle, editorial, global_ = cargar_datos_desde_mysql()
    python = calcular_ganancias_en_python(detalle)
    ok, comparacion = comparar_sql_vs_python(sql, python)
    imprimir_resultados(
        resultado_sql=sql,
        resultado_python=python,
        comparacion=comparacion,
        validacion_ok=ok,
        vista_editorial=editorial,
        comparacion_global=global_,
    )
    return ok


def practica4():
    from practica4.conexion import cargar_datos_desde_mysql
    from practica4.calculo import calcular_maximos_en_python
    from practica4.comparacion import comparar_sql_vs_python
    from practica4.reporte import imprimir_resultados

    sql, detalle, global_ = cargar_datos_desde_mysql()
    python = calcular_maximos_en_python(detalle)
    ok, comparacion = comparar_sql_vs_python(sql, python)
    imprimir_resultados(
        resultado_sql=sql,
        resultado_python=python,
        comparacion=comparacion,
        validacion_ok=ok,
        comparacion_global=global_,
    )
    return ok


def practica5():
    from practica5.conexion import cargar_datos_desde_mysql
    from practica5.calculo import (
        calcular_top_clientes_en_python,
        calcular_top_productos_en_python,
    )
    from practica5.comparacion import (
        comparar_clientes_sql_vs_python,
        comparar_productos_sql_vs_python,
    )
    from practica5.reporte import imprimir_resultados

    productos_sql, clientes_sql, detalle, global_ = cargar_datos_desde_mysql()
    productos_python = calcular_top_productos_en_python(detalle)
    clientes_python = calcular_top_clientes_en_python(detalle, productos_python)

    ok_productos, comparacion_productos = comparar_productos_sql_vs_python(
        productos_sql, productos_python
    )
    ok_clientes, comparacion_clientes = comparar_clientes_sql_vs_python(
        clientes_sql, clientes_python
    )

    imprimir_resultados(
        top_productos_sql=productos_sql,
        top_productos_python=productos_python,
        comparacion_productos=comparacion_productos,
        ok_productos=ok_productos,
        top_clientes_sql=clientes_sql,
        top_clientes_python=clientes_python,
        comparacion_clientes=comparacion_clientes,
        ok_clientes=ok_clientes,
        comparacion_global=global_,
    )
    return ok_productos and ok_clientes


# Para agregar otra práctica: pon el número, el nombre y la función.
PRACTICAS = {
    "3": ("Ganancias por autor", practica3),
    "4": ("Producto top por año y región", practica4),
    "5": ("Producto top por región y clientes top", practica5),
}


def main():
    print("\n¿Qué práctica quieres ejecutar?\n")
    for numero, (nombre, _) in sorted(PRACTICAS.items(), key=lambda x: int(x[0])):
        print(f"  {numero} - {nombre}")

    opcion = input("\nEscribe el número: ").strip()

    if opcion not in PRACTICAS:
        print(f"\nOpción no válida: {opcion!r}")
        return 1

    nombre, ejecutar = PRACTICAS[opcion]
    print(f"\nEjecutando práctica {opcion}: {nombre}...\n")
    ok = ejecutar()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
