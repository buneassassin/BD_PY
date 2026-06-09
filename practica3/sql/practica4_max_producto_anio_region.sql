-- Práctica 4 - Base de datos: tienda (Pubs)
-- Producto con mayor ganancia por año y región (estado de la tienda)
--
-- Requisitos:
--   - Exactamente 3 tablas en el FROM: sales, titles, stores
--   - Agregado MAX sobre ganancias por producto (sin vistas ni procedimientos)
--   - Sin subconsultas escalares en WHERE; una sola sentencia SELECT
--
-- Fórmula por línea de venta:
--   ganancia = cantidad_vendida * precio_título
--
-- Región = stores.state
-- Año    = primeros 4 caracteres de sales.ord_date (YYYYMMDD)

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
ORDER BY p.Anio, p.Region;
