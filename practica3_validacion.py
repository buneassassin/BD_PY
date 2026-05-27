"""
Practica 3 - Validacion SQL vs Python
"""

from __future__ import annotations

from practica3.calculo import calcular_ganancias_en_python
from practica3.comparacion import comparar_sql_vs_python
from practica3.conexion import cargar_datos_desde_mysql
from practica3.reporte import imprimir_resultados


def ejecutar_validacion() -> bool:
    
    resultado_sql, ventas_detalle = cargar_datos_desde_mysql()
    resultado_python = calcular_ganancias_en_python(ventas_detalle)
    validacion_ok, comparacion = comparar_sql_vs_python(resultado_sql, resultado_python)

    imprimir_resultados(
        resultado_sql=resultado_sql,
        resultado_python=resultado_python,
        comparacion=comparacion,
        validacion_ok=validacion_ok,
    )
    return validacion_ok


def main() -> None:
    ejecutar_validacion()


if __name__ == "__main__":
    main()
