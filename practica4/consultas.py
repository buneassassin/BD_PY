"""
Consultas de la practica 4 (solo sales, titles, stores):

  1) CONSULTA_SQL              -> MAX por año y región (resultado principal)
  2) CONSULTA_PY               -> detalle fila a fila para Python
  3) CONSULTA_TOTAL_AGRUPADO   -> suma global con las 3 tablas (todos los productos)
  4) CONSULTA_TOTAL_VENTAS     -> suma global sales + titles
  5) CONSULTA_SIN_TIENDA       -> ventas sin tienda en stores
  6) CONSULTA_RESUMEN_ANIO     -> totales por año (auditoría)
"""

CONSULTA_SQL = """
SELECT
    p.Anio,
    p.Region,
    p.Producto,
    p.Ganancia
FROM (
    SELECT
        SUBSTRING(s.ord_date, 1, 4) AS Anio,
        st.state AS Region,
        t.title_id AS Producto,
        SUM(s.qty * t.price) AS Ganancia
    FROM sales AS s
    INNER JOIN titles AS t ON s.title_id = t.title_id
    INNER JOIN stores AS st ON s.stor_id = st.stor_id
    GROUP BY Anio, Region, Producto
) AS p
INNER JOIN (
    SELECT
        Anio,
        Region,
        MAX(Ganancia) AS Ganancia_max
    FROM (
        SELECT
            SUBSTRING(s.ord_date, 1, 4) AS Anio,
            st.state AS Region,
            t.title_id AS Producto,
            SUM(s.qty * t.price) AS Ganancia
        FROM sales AS s
        INNER JOIN titles AS t ON s.title_id = t.title_id
        INNER JOIN stores AS st ON s.stor_id = st.stor_id
        GROUP BY Anio, Region, Producto
    ) AS por_producto
    GROUP BY Anio, Region
) AS m ON p.Anio = m.Anio
    AND p.Region = m.Region
    AND p.Ganancia = m.Ganancia_max
ORDER BY p.Anio, p.Region
"""

CONSULTA_PY = """
SELECT
    SUBSTRING(s.ord_date, 1, 4) AS Anio,
    st.state AS Region,
    t.title_id AS Producto,
    s.stor_id,
    s.ord_num,
    s.qty,
    t.price
FROM sales AS s
INNER JOIN titles AS t ON s.title_id = t.title_id
INNER JOIN stores AS st ON s.stor_id = st.stor_id
ORDER BY Anio, Region, Producto, s.ord_num
"""

CONSULTA_TOTAL_AGRUPADO = """
SELECT SUM(s.qty * t.price) AS Ganancia_agrupada
FROM sales AS s
INNER JOIN titles AS t ON s.title_id = t.title_id
INNER JOIN stores AS st ON s.stor_id = st.stor_id
"""

CONSULTA_TOTAL_VENTAS = """
SELECT SUM(s.qty * t.price) AS Ganancia_ventas_general
FROM sales AS s
INNER JOIN titles AS t ON t.title_id = s.title_id
"""

CONSULTA_SIN_TIENDA = """
SELECT SUM(s.qty * t.price) AS total_sin_tienda
FROM sales AS s
INNER JOIN titles AS t ON t.title_id = s.title_id
LEFT JOIN stores AS st ON s.stor_id = st.stor_id
WHERE st.stor_id IS NULL
"""

CONSULTA_RESUMEN_ANIO = """
SELECT
    SUBSTRING(s.ord_date, 1, 4) AS Anio,
    SUM(s.qty * t.price) AS Ganancia_anio
FROM sales AS s
INNER JOIN titles AS t ON s.title_id = t.title_id
INNER JOIN stores AS st ON s.stor_id = st.stor_id
GROUP BY Anio
ORDER BY Anio
"""
